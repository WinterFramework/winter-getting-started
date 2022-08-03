import winter
import winter_django
import winter_openapi
from winter_django.autodiscovery import create_django_urls_for_package
from winter.core import set_injector
from injector import Injector

set_injector(Injector())

winter.web.setup()
winter_django.setup()
winter_openapi.setup(allow_missing_raises_annotation=True)

urlpatterns = [
    *create_django_urls_for_package('simple_api'),
]
