"""All views are defined here. Implementation must go to lib."""
import json
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

from django.contrib.auth.decorators import login_required
from django.db import transaction, DatabaseError, IntegrityError, Error
from django.db.models.deletion import ProtectedError
from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_GET, require_POST, require_http_methods

import fixture
import fixture.modules.api as api_lib
from fixture.models import (
    Session, SessionStatus, FixtureInstance, FixtureInstanceStatus, FixtureDefs, Resource, ResourceContent, ResourceType
)
from fixture.views.models import (
    TestSessionRequest, CreateFixtureInstanceRequest, CreateResourceRequest, GetResourceRequest, DeleteResourceRequest,
    DeleteFixtureInstanceRequest
)

LOGGER = logging.getLogger(__name__)


@login_required
@requires_csrf_token
@require_GET
def fixture_list(request: HttpRequest) -> List[str]:
    """List all known fixtures."""
    return JsonResponse(data={"data": api_lib.list_fixtures()})


@login_required
@requires_csrf_token
@require_GET
def list_test_sessions(request: HttpRequest):
    """List test sessions."""
    all_sessions = Session.objects.all().filter(is_deleted=False)
    LOGGER.debug("Found %d active sessions.", len(all_sessions))
    session_dict = {
        "data": [model_to_dict(session) for session in all_sessions]
    }
    return JsonResponse(data=session_dict)


@login_required
@require_POST
def create_resource(request: HttpRequest):
    """Create resource."""
    req_json = json.loads(request.body)
    create_res_req = CreateResourceRequest(**req_json)

    error_msg = "Unknown Error"
    status_code = 500
    try:
        # get resource type. currently only json is available / implemented
        res_type = ResourceType(create_res_req.resource_type)
        # verify json content
        json.loads(create_res_req.content)
        with transaction.atomic():
            # create resource content
            rcontent = ResourceContent(data=bytearray(create_res_req.content, encoding="utf-8"))
            rcontent.save()
            # create resource
            res = Resource(resource_type=res_type, content=rcontent)
            res.save()
            return JsonResponse(model_to_dict(res))
    except (json.decoder.JSONDecodeError, DatabaseError) as exc:
        error_msg = exc.args[0]
    except ValueError as exc:
        error_msg = exc.args[0]
        status_code = 404
    return JsonResponse({"error": error_msg}, status=status_code)


@login_required
@require_GET
def get_resource(request: HttpRequest):
    """
    Get resource.

    Notes
    -----
    1. For document resources, returns the content.
    2. Future resource type content would need to be handled as required,

    """
    req_json = json.loads(request.body)
    try:
        get_res_req = GetResourceRequest(**req_json)
        res_id = get_res_req.query.identifier
        res = Resource.objects.filter(id=res_id).first()
        return JsonResponse({
            "idenitfier": res.id,
            "resource_type": res.resource_type,
            "content": bytes(res.content.data).decode(encoding="utf-8")
        })
    except (ValueError, AttributeError) as exc:
        return JsonResponse({"error": exc.args[0]}, status=404)


@login_required
@require_http_methods(["DELETE"])
def delete_resource(request: HttpRequest):
    """Delete resource."""
    req_json = json.loads(request.body)
    try:
        del_res_req = DeleteResourceRequest(**req_json)
        res_id = del_res_req.identifier
        content_id = None
        with transaction.atomic():
            res_obj = Resource.objects.filter(id=res_id).first()
            content_id = res_obj.content.id
            res_obj.delete()

        with transaction.atomic():
            if content_id is not None:
                res_content_obj = ResourceContent.objects \
                    .filter(id=content_id) \
                    .select_for_update() \
                    .first()
                count = Resource.objects.filter(content=res_content_obj).count()
                if count == 0:
                    res_content_obj.delete()
    except IntegrityError as exc:
        if not isinstance(exc, ProtectedError):
            return JsonResponse({"error": exc.args[0]}, status=500)
    except (ValueError, AttributeError) as exc:
        return JsonResponse({"error": exc.args[0]}, status=404)
    return JsonResponse(data=None)


@login_required
@requires_csrf_token
@require_http_methods(["POST"])
def session_start(request: HttpRequest):
    """Start a new session."""
    req_body: Dict[str, Any] = json.loads(request.body)

    # validate the request body
    session_req = TestSessionRequest(**req_body)

    # create a new test session
    new_session = Session(
        name=session_req.name,
        description=session_req.description,
        status=SessionStatus.CREATED,
        created_at=datetime.now(tz=timezone.utc),
        updated_at=None,
        exit_code=None,
        is_deleted=False,
        message=None)
    new_session.save()
    LOGGER.debug("Created new test session: %s", new_session.id)
    return JsonResponse(data=model_to_dict(new_session))


@login_required
@require_http_methods(["POST"])
def session_end(request: HttpRequest, session_id: str):
    """End session with given session id."""
    try:
        message = "success"
        status_code = 200
        # check if session id is valid and status is valid
        session = Session.objects.get(id=session_id)
        if session.status < 4:
            # Mark Session status to FINISHING
            session.status = SessionStatus.FINISHING
            session.save()
    except Error as exc:
        message = exc.args[0]
        status_code = 404
    return JsonResponse(data=message, status=status_code)


@login_required
@require_http_methods(["POST"])
def session_new_fixture_instance(request: HttpRequest, session_id: str):
    """Create a new fixture instance for given session id."""
    # verify and create request for acquiring a fixture
    req_json = json.loads(request.body)
    fixture_request = CreateFixtureInstanceRequest(**req_json)
    fdef = FixtureDefs.objects.get(namespace=fixture_request.namespace, name=fixture_request.name)
    if fdef is None:
        return JsonResponse(data={"error": "Fixture not found!"}, status=404)

    msg = "Unknonw"
    status_code = 500
    try:
        with transaction.atomic():
            # check session state
            session_obj = Session.objects.filter(id=session_id).select_for_update().first()
            if session_obj is None or session_obj.status >= SessionStatus.FINISHING:
                return JsonResponse(data={"error": "Invalid session or session status"}, status=404)
            instance = FixtureInstance.objects \
                .filter(session_id=session_id) \
                .select_for_update() \
                .get(fixture_def_id=fdef.id)
            # case I: fixture instance already exists.
            if instance is not None:
                return JsonResponse(data={"error": f"Instance already exists: {instance.id}"}, status=404)

            # case II: fixture instance does not exists.
            instance = FixtureInstance(
                status=FixtureInstanceStatus.CREATED,
                created_at=datetime.now(tz=timezone.utc),
                updated_at=None,
                message=None,
                fixture_def_id=fdef.id,
                session_id=session_id)
            instance.save()
            instance_info = model_to_dict(instance)
            return JsonResponse(data=instance_info)
    except ValueError as exc:
        msg = exc.args[0]
        status_code = 404
    except Error as exc:
        msg = exc.args[0]
        status_code = 500
    return JsonResponse(data={"error": msg}, status=status_code)


@login_required
@require_http_methods(["POST"])
def session_delete_fixture_instance(request: HttpRequest, session_id: str):
    """Delete the fixture instance for given session id."""
    message = "Unknown"
    status_code = 500
    try:
        req_json = json.loads(request.body)
        fixture_request = DeleteFixtureInstanceRequest(**req_json)
        with transaction.atomic():
            # verify if session id is a valid session id
            session_obj = Session.objects.get(id=session_id)
            if session_obj is None or session_obj.status != SessionStatus.STARTED:
                return JsonResponse(data={"error": "Invalid session or session status"}, status=404)

            # verify whether the fixture instance exists
            fixture_instance = FixtureInstance.objects \
                .filter(session_id=session_id) \
                .select_for_update() \
                .get(id=fixture_request.identifier)

            if fixture_instance.status not in (
                    FixtureInstanceStatus.SETUP_FINISHED, FixtureInstanceStatus.SETUP_FAILED):
                return JsonResponse(data={"error": "Invalid fixture status"}, status=404)
            # Else the instance must be marked to be PENDING_TEARDOWN
            fixture_instance.status = FixtureInstanceStatus.TEARDOWN_PENDING
            fixture_instance.updated_at = datetime.now(tz=timezone.utc)
            fixture_instance.save()
            return JsonResponse(data=None)
    except (fixture.models.FixtureInstance.DoesNotExist, fixture.models.Session.DoesNotExist) as exc:
        status_code = 404
        message = exc.args[0]
    except Error as exc:
        status_code = 500
        message = exc.args[0]
    return JsonResponse(data={"error": message}, status=status_code)


@login_required
@require_http_methods(["GET"])
def session_list_fixture_instances(request: HttpRequest, session_id: str):
    """List fixture instances for given session id."""


@login_required
@require_http_methods(["GET"])
def session_get_fixture_instance(request: HttpRequest, session_id: str):
    """session_get_fixture_instance for given session id."""


@login_required
@require_http_methods(["GET", "POST", "DELETE"])
def session_get_resource_by_fixture_instance(request: HttpRequest, session_id: str):
    """session_get_resource_by_fixture_instance for given session id."""
