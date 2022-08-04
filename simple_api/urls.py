from winter_django.autodiscovery import create_django_urls_for_package
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


urlpatterns = [
    *create_django_urls_for_package('simple_api'),
]

schema_view = get_schema_view(
    openapi.Info(title='Getting Started Winter API', default_version='v1'),
    patterns=urlpatterns,
)
urlpatterns += [
    re_path(r'^$', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
]
