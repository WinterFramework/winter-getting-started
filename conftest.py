import httpx
import pytest

from simple_api.wsgi import application


@pytest.fixture()
def api_client():
    transport = httpx.WSGITransport(app=application)
    with httpx.Client(transport=transport, base_url='http://127.0.0.1') as client:
        yield client
