![Tests](https://github.com/WinterFramework/winter-getting-started/actions/workflows/test.yml/badge.svg?event=push)

How to start project with Winter
--------------------------------
Winter needs Python 3.11 or newer.

Bootstrap empty project
```shell
$ poetry init
$ poetry add winter
$ poetry run django-admin startproject simple_api .
```

Add `simple_api/api.py` with contents:
```python
from http import HTTPStatus

import winter.web


@winter.web.problem(status=HTTPStatus.BAD_REQUEST)
class NameTooLongException(Exception):
    def __init__(self, max_length: int):
        super().__init__(f'Name must be at most {max_length} characters long')


class SimpleAPI:
    @winter.web.route_get('greeting/')
    def greeting(self) -> str:
        return 'Hello from Winter API!'

    @winter.web.route_get('greeting/{name}/')
    @winter.web.raises(NameTooLongException)
    def personal_greeting(self, name: str) -> str:
        if len(name) > 20:
            raise NameTooLongException(max_length=20)
        return f'Hello, {name}!'
```

Replace `simple_api/urls.py` with:
```python
import winter.django
import winter.web

routes = winter.web.find_package_routes('simple_api.api')
urlpatterns = winter.django.create_django_urls_from_routes(routes)
```

Add `simple_api/apps.py` with contents:
```python
from django.apps import AppConfig


class SimpleApiConfig(AppConfig):
    name = 'simple_api'

    def ready(self):
        import winter.application
        import winter.django
        import winter.openapi
        import winter.web
        from injector import Injector

        # Import the URLs first: route discovery imports every API module, so the setup calls
        # below see all @problem exceptions and @raises annotations.
        import simple_api.urls  # noqa: F401

        winter.application.set_injector(Injector())
        winter.web.setup()
        winter.django.setup()
        winter.openapi.setup(allow_missing_raises_annotation=True)
```

The order matters. Setup registers handlers only for the exception classes that are already
imported, so call it after the routes are discovered, not from `settings.py`.

Add `'simple_api'` to `INSTALLED_APPS` in `settings.py`.

Add OpenAPI and Swagger UI
--------------------------

Add `simple_api/openapi.py` with contents:
```python
import winter.openapi
import winter.web


class OpenAPI:
    @winter.web.route_get('openapi.json')
    def openapi(self):
        """OpenAPI specification"""
        routes = winter.web.find_package_routes('simple_api.api')
        return winter.openapi.generate_openapi(
            'Getting Started Winter API',
            'v1',
            routes,
        )

    @winter.web.route_get('')
    def swagger_ui(self) -> winter.web.Response:
        """HTML page with Swagger UI"""
        html = winter.openapi.get_swagger_ui_html(openapi_url='/openapi.json')
        return winter.web.Response(200, body=html.encode(), headers={'content-type': 'text/html'})
```

Add its routes in `simple_api/urls.py`:
```python
routes = [
    *winter.web.find_package_routes('simple_api.api'),
    *winter.web.find_package_routes('simple_api.openapi'),
]
```

`find_package_routes` takes a module or a package. A package is scanned with all its modules, so do not
scan `simple_api` itself: that would import `wsgi.py` and the settings during setup.

How to run
----------

You can use any WSGI server, for example gunicorn:

```shell
$ poetry add gunicorn
$ poetry run gunicorn simple_api.wsgi
```

Check it's working http://localhost:8000/greeting/

```shell
$ http get http://localhost:8000/greeting/
```

Expected output:
```
HTTP/1.1 200 OK
Server: gunicorn
Date: Mon, 12 Oct 2026 16:53:43 GMT
Connection: close
content-type: application/json
X-Frame-Options: DENY
Content-Length: 24
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

"Hello from Winter API!"
```

A name that is too long returns a problem response in accordance with [RFC 7807](https://tools.ietf.org/html/rfc7807):

```shell
$ http get http://localhost:8000/greeting/a-name-that-is-way-too-long/
```

```
HTTP/1.1 400 Bad Request
Content-Type: application/problem+json

{
    "detail": "Name must be at most 20 characters long",
    "status": 400,
    "title": "Name too long",
    "type": "urn:problem-type:name-too-long"
}
```

Swagger UI is at http://localhost:8000/

How to test
-----------

```shell
$ poetry install
$ poetry run pytest
```

See [conftest.py](conftest.py) for an `httpx` client that calls the WSGI application in-process.

How to deploy to GKE
--------------------

The repository contains the example deployment to GKE. Files of interest:
- [Dockerfile](Dockerfile) - Dockerfile to build the application image
- [deployment.yaml](deployment.yaml) - k8s deployment configuration
- [.github/workflows/gke.yml](.github/workflows/gke.yml) - GitHub workflow to automatically deploy the application to GKE on push to master
