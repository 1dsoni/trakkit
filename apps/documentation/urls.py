from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Trakkit APIs",
        default_version='v1',
        description="Apis description",
        terms_of_service="https://github.com/1dsoni/trakkit/tree/main",
        contact=openapi.Contact(
            email="diwanshusoni96@gmail.com",
            name='admin',
            url='https://github.com/1dsoni/trakkit/tree/main'
        ),
        license=openapi.License(name="BSD License")
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
