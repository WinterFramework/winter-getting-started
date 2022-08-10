import django
import pytest
import os
from django.test import LiveServerTestCase


@pytest.fixture(scope='session')
def live_server_url():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_api.settings')
    django.setup()
    LiveServerTestCase.setUpClass()
    yield LiveServerTestCase.live_server_url
    LiveServerTestCase.tearDownClass()
