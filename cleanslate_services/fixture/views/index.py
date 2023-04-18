"""All views are defined here. Implementation must go to lib."""
from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token

import fixture.lib.api as api_lib


@login_required
@requires_csrf_token
def render_index(request: HttpRequest):
    """Render the landing page."""
    # get list of fixtures
    ctx: Dict[str, Any] = {
        'fixture_list': api_lib.list_fixtures()
    }
    return render(request=request, template_name="index.html", context=ctx)
