"""All views are defined here. Implementation must go to lib."""
from typing import List

from django.http import HttpResponse
from django.shortcuts import render

import fixture.lib.api as api_lib

# Create your views here.


def fixture_list(request):
    """List all known fixtures."""
    all_fixtures: List[str] = api_lib.list_fixtures()
    return HttpResponse(str(all_fixtures))
