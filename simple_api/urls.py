import winter
import winter_django
import winter_openapi
from winter_django.autodiscovery import create_django_urls_for_package
from winter.core import set_injector
from injector import Injector
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


set_injector(Injector())

winter.web.setup()
winter_django.setup()
winter_openapi.setup(allow_missing_raises_annotation=True)

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
