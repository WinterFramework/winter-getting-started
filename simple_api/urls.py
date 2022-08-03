from winter_django.autodiscovery import create_django_urls_for_package
from winter.core import set_injector
from injector import Injector

set_injector(Injector())

urlpatterns = [
    *create_django_urls_for_package('simple_api'),
]
