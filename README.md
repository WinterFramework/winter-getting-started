![Tests](https://github.com/WinterFramework/winter-getting-started/actions/workflows/test.yml/badge.svg?event=push)

[Deployed Demo](https://getting-started.winter-framework.org/)

How to start project with Winter
--------------------------------
Bootstrap empty project
```shell
$ poetry init
$ poetry add winter
$ poetry run django-admin startproject simple_api .
```

Add `rest_framework` to `settings.INSTALLED_APPS`

Add `simple_api/api.py` with contents:
```python
import winter


@winter.web.no_authentication
class SimpleAPI:
    @winter.route_get('greeting/')
    def greeting(self) -> str:
        return 'Hello from Winter API!'
```

Modify `urls.py` to the following:
```python
from winter.web import find_package_routes
from winter_django import create_django_urls_from_routes

routes = find_package_routes('simple_api')
urlpatterns = create_django_urls_from_routes(routes)

```

Add the following code to `settings.py`
```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'winter_django.renderers.JSONRenderer',
    ],
}

import winter.core
import winter_django
import winter_openapi
from injector import Injector


winter.core.set_injector(Injector())
winter.web.setup()
winter_django.setup()
winter_openapi.setup(allow_missing_raises_annotation=True)
```

Add OpenAPI and Swagger UI
--------------------------

Add `src/openapi.py` with the following contents:
```python
import winter
import winter_openapi
from django.http import HttpResponse
from winter.web import find_package_routes


@winter.web.no_authentication
class OpenAPI:
    @winter.route_get('openapi.json')
    def openapi(self):
        """OpenAPI specification"""
        routes = find_package_routes('simple_api.api')
        return winter_openapi.generate_openapi(
            'Getting Started Winter API',
            'v1',
            routes,
        )

    @winter.route_get('')
    def swagger_ui(self):
        """HTML page with Swagger UI"""
        html = winter_openapi.get_swagger_ui_html(openapi_url='/openapi.json')
        return HttpResponse(html, content_type='text/html')

```

How to run
----------

You can use any WSGI server, for example gunicorn or waitress:

```shell
$ poetry add gunicorn
$ poetry run gunicorn simple_api:wsgi
```

Check it's working http://localhost:8000/greeting/

```shell
$ http get http://localhost:8000/greeting/
```

Expected output:
```
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Length: 24
Content-Type: application/json
Date: Wed, 03 Aug 2022 21:44:55 GMT
Server: WSGIServer/0.2 CPython/3.8.7
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

"Hello from Winter API!"
```

How to deploy to Heroku
-----------------------
First create a Heroku application and basic configuration required for python

```shell
$ heroku apps:create winter-getting-started
```

Add poetry buildpack for Heroku:
```shell
$ heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
$ heroku buildpacks:add heroku/python
```

Add `Procfile` with contents:
```
web: gunicorn simple_api.wsgi
```

Add heroku hosts to settings.ALLOWED_HOSTS
```
ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']
```

Then push the current version to deploy it

```shell
$ git push heroku master
```

Check it's working https://winter-getting-started.herokuapp.com/greeting/
```shell
$ http get https://winter-getting-started.herokuapp.com/greeting/
```

Expected output:
```
HTTP/1.1 200 OK 
Allow: GET, HEAD, OPTIONS
Connection: keep-alive
Content-Length: 24
Content-Type: application/json
Date: Wed, 03 Aug 2022 22:51:26 GMT
Server: gunicorn
Vary: Cookie
Via: 1.1 vegur
X-Frame-Options: SAMEORIGIN

"Hello from Winter API!"
```
