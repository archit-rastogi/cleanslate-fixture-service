from django.contrib import admin  # noqa

from .models import Session, FixtureDefs, FixtureInstance, Resource

# Register your models here.
admin.site.register(Session)
admin.site.register(FixtureDefs)
admin.site.register(FixtureInstance)
admin.site.register(Resource)
