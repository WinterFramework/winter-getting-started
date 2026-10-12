import httpx


def test_openapi_lists_greeting_endpoints(api_client: httpx.Client):
    http_response = api_client.get('/openapi.json')
    assert http_response.status_code == 200
    assert set(http_response.json()['paths']) == {'/greeting/', '/greeting/{name}/'}


def test_swagger_ui(api_client: httpx.Client):
    http_response = api_client.get('/')
    assert http_response.status_code == 200
    assert http_response.headers['content-type'].startswith('text/html')
