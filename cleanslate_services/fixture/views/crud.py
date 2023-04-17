"""All views are defined here. Implementation must go to lib."""
from typing import List

import fixture.lib.api as api_lib
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_GET


@login_required
@requires_csrf_token
@require_GET
def fixture_list(request: HttpRequest) -> List[str]:
    """List all known fixtures."""
    return JsonResponse(data={"data": api_lib.list_fixtures()})
