import httpx


def test_greeting(api_client: httpx.Client):
    http_response = api_client.get('/greeting/')
    assert http_response.status_code == 200
    assert http_response.json() == 'Hello from Winter API!'


def test_404(api_client: httpx.Client):
    http_response = api_client.get('/intentionally-wrong-url/')
    assert http_response.status_code == 404
