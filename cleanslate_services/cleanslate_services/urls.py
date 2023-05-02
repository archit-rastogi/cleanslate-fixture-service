"""
URL configuration for cleanslate_services project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import fixture.views.crud as crud_view
import fixture.views.index as index_view

urlpatterns = [
    path("", index_view.render_index),
    path("admin/", admin.site.urls),
    path("get_cards", index_view.get_cards),
    path("get_card_details/<str:card_id>", index_view.get_card_details),

    path("fixture/list", crud_view.fixture_list),

    path("session/start", crud_view.session_start),
    path("session/<str:session_id>/end", crud_view.session_end),
    path("session/<str:session_id>/fixture/instance/new", crud_view.session_new_fixture_instance),
    path("session/<str:session_id>/fixture/instance/delete", crud_view.session_delete_fixture_instance),
    path("session/<str:session_id>/fixture/instance/list", crud_view.session_list_fixture_instances),
    # path("session/<str:session_id>/resources/list", None),

    path("fixture/instance/<str:instance_id>", crud_view.fixture_get_instance),
    path("fixture/instance/<str:instance_id>/resource", crud_view.fixture_get_resource_by_instance),

    path("resource/create", crud_view.create_resource),
    path("resource/<str:identifier>", crud_view.get_resource),
    # path("resource/list", crud_view.list_resources),
    path("resource/<str:identifier>/delete", crud_view.delete_resource)
]
