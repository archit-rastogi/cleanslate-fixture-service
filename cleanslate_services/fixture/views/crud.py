"""All views are defined here. Implementation must go to lib."""
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_GET, require_POST

import fixture.lib.api as api_lib
from fixture.models import TestSession, TestSessionStatus, FixtureInstance, FixtureInstanceStatus
from fixture.views.models import TestSessionRequest, AcquireFixtureInstanceRequest

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
def acquire_fixture_instance(request: HttpRequest):
    """Acquires a lock on fixture instance."""
    # verify and create request for acquiring a fixture
    req_json = json.loads(request.body)
    acquire_request = AcquireFixtureInstanceRequest(**req_json)

    # internal fixture
    fix_class = api_lib.get_fixture_class(acquire_request.namespace, acquire_request.name)
    # upsert the internal fixture def

    instance = FixtureInstance(
        status=FixtureInstanceStatus.CREATED,
        created_at=datetime.now(),
        updated_at=None,
        message=None,
        fixture_def_id=None,
        session_id=acquire_request.session_id
    )
    instance.save()

    # fixture_def_id = FixtureDefs.objects.filter(
    #     namespace=acquire_request.namespace,
    #     name=acquire_request.name).first().id



def yield_fixture_instance(request: HttpRequest):
    """Yields the lock on fixture to be later acquired by other processes."""
