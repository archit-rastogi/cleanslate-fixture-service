"""All views are defined here. Implementation must go to lib."""
import json
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

from django.contrib.auth.decorators import login_required
from django.db import transaction, DatabaseError
from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_GET, require_POST

import fixture.lib.api as api_lib
from fixture.models import (
    TestSession, TestSessionStatus, FixtureInstance, FixtureInstanceStatus, FixtureDefs, Resource, ResourceContent,
    ResourceType
)
from fixture.views.models import TestSessionRequest, CreateFixtureInstanceRequest, CreateResourceRequest

LOGGER = logging.getLogger(__name__)


@login_required
@requires_csrf_token
@require_GET
def fixture_list(request: HttpRequest) -> List[str]:
    """List all known fixtures."""
    return JsonResponse(data={"data": api_lib.list_fixtures()})


@login_required
@requires_csrf_token
@require_POST
def create_test_session(request: HttpRequest):
    """Create a new test session."""
    req_body: Dict[str, Any] = json.loads(request.body)

    # validate the request body
    session_req = TestSessionRequest(**req_body)

    # create a new test session
    new_session = TestSession(
        name=session_req.name,
        description=session_req.description,
        status=TestSessionStatus.CREATED,
        created_at=datetime.now(),
        updated_at=None,
        exit_code=None,
        is_deleted=False,
        message=None)
    new_session.save()
    LOGGER.debug("Created new test session: %s", new_session.id)
    return JsonResponse(data=model_to_dict(new_session))


@login_required
@requires_csrf_token
@require_GET
def list_test_sessions(request: HttpRequest):
    """List test sessions."""
    all_sessions = TestSession.objects.all().filter(is_deleted=False)
    LOGGER.debug("Found %d active sessions.", len(all_sessions))
    session_dict = {
        "data": [model_to_dict(session) for session in all_sessions]
    }
    return JsonResponse(data=session_dict)


@login_required
@requires_csrf_token
@require_POST
def create_fixture_instance(request: HttpRequest):
    """Acquires a lock on fixture instance."""
    # verify and create request for acquiring a fixture
    req_json = json.loads(request.body)
    acquire_request = CreateFixtureInstanceRequest(**req_json)

    fdef = FixtureDefs.objects.filter(namespace=acquire_request.namespace, name=acquire_request.name).first()
    if fdef is None:
        return JsonResponse(data={"error": "Fixture not found!"}, status=404)

    instance = FixtureInstance(
        status=FixtureInstanceStatus.CREATED,
        created_at=datetime.now(tz=timezone.utc),
        updated_at=None,
        message=None,
        fixture_def_id=None,
        session_id=TestSession.objects.filter(id=acquire_request.session_id).first()
    )
    instance.save()
    instance_info = model_to_dict(instance)
    return JsonResponse(data=instance_info)


@login_required
@require_POST
def create_resource(request: HttpRequest):
    """Create resource."""
    req_json = json.loads(request.body)
    create_res_req = CreateResourceRequest(**req_json)

    error_msg = "Unknown Error"
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
    except (json.decoder.JSONDecodeError, DatabaseError, ValueError) as exc:
        error_msg = exc.args[0]
    return JsonResponse({"error": error_msg}, status=500)


@login_required
@require_GET
def get_resource(request: HttpRequest):
    """Get resource."""


@login_required
@require_GET
def list_resources(request: HttpRequest):
    """List_ esources."""


@login_required
def delete_resource(request: HttpRequest):
    """Delete resource."""
