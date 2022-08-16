import pytest
import httpx
from wsgi import application


@pytest.fixture()
def api_client():
    with httpx.Client(app=application, base_url='http://127.0.0.1') as client:
        yield client
