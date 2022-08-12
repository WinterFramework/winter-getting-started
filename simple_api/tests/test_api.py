import requests


def test_simple_api(live_server_url: str):
    client = requests.Session()
    http_response = client.get(f'{live_server_url}/greeting/')

    assert http_response.status_code == 200
    assert http_response.json() == 'Hello from Winter API!'
