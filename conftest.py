import django
import pytest
import os
import httpx
from simple_api.wsgi import application


@pytest.fixture(scope='session')
def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_api.settings')
    django.setup()


@pytest.fixture()
def api_client(setup_django):
    with httpx.Client(app=application, base_url='http://127.0.0.1') as client:
        yield client
