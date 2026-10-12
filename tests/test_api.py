import httpx


def test_greeting(api_client: httpx.Client):
    http_response = api_client.get('/greeting/')
    assert http_response.status_code == 200
    assert http_response.json() == 'Hello from Winter API!'


def test_personal_greeting(api_client: httpx.Client):
    http_response = api_client.get('/greeting/Winter/')
    assert http_response.status_code == 200
    assert http_response.json() == 'Hello, Winter!'


def test_problem_is_returned_for_too_long_name(api_client: httpx.Client):
    http_response = api_client.get('/greeting/a-name-that-is-way-too-long/')
    assert http_response.status_code == 400
    assert http_response.headers['content-type'] == 'application/problem+json'
    assert http_response.json()['detail'] == 'Name must be at most 20 characters long'


def test_404(api_client: httpx.Client):
    http_response = api_client.get('/intentionally-wrong-url/')
    assert http_response.status_code == 404
