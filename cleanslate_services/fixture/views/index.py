"""All views are defined here. Implementation must go to lib."""
from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_GET

import fixture.modules.api as api_lib
from fixture.views.constants import CardIds


@login_required
@requires_csrf_token
def render_index(request: HttpRequest):
    """Render the landing page."""
    return render(request=request, template_name="index.html", context={})


@require_GET
def get_cards(request: HttpRequest):
    """Render index page and load all cards."""
    ctx: Dict[str, Any] = {
        "cards": [
            {
                "name": CardIds.REMOTE_FIXTURES,
                "title": "Remote Fixtures",
                "summary": "",
                "action": "Browse"
            },
            {
                "name": CardIds.REMOTE_RESOURCES,
                "title": "Remote Resources",
                "summary": "",
                "action": "Browse"
            },
            {
                "name": CardIds.ANALYZE,
                "title": "Analyze",
                "summary": "",
                "action": "Go To Dashboard"
            }
        ]
    }
    return render(request=request, template_name="cards.html", context=ctx)


@require_GET
def get_card_details(request: HttpRequest, card_id: str):
    """Get card details by id."""
    card_id = CardIds.REMOTE_FIXTURES
    template_name = "error.html"
    ctx: Dict[str, Any] = {}
    if card_id == CardIds.REMOTE_FIXTURES:
        # get list of fixtures
        ctx = {
            'fixture_list': api_lib.list_fixtures()
        }
        template_name = "browse_fixtures.html"
    return render(request=request, template_name=template_name, context=ctx)
