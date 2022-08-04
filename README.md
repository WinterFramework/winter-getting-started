How to start project with Winter
--------------------------------
1. Bootstrap empty project
```shell
$ poetry init
$ poetry add winter
$ poetry run django-admin startproject simple_api .
```

2. Add `rest_framework` to `settings.INSTALLED_APPS`
3. Add `simple_api/api.py` with contents:
```python
import winter


@winter.web.no_authentication
class SimpleAPI:
    @winter.route_get('greeting/')
    def greeting(self) -> str:
        return 'Hello from Winter API!'
```

4. Add the following code to `simple_api/__init__.py`:
```python
import winter
import winter_django
import winter_openapi
from winter_django.autodiscovery import create_django_urls_for_package
from winter.core import set_injector
from injector import Injector

set_injector(Injector())

winter.web.setup()
winter_django.setup()
winter_openapi.setup(allow_missing_raises_annotation=True)

urlpatterns = [
    *create_django_urls_for_package('simple_api'),
]
```

5. Modify `urls.py` to the following:
```python
from winter_django.autodiscovery import create_django_urls_for_package

urlpatterns = [
    *create_django_urls_for_package('simple_api'),
]
```

6. Enable winter JSON capabilities by adding the following code to `settings.py`
```
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'winter_django.renderers.JSONRenderer',
    ],
}
```

7. Add Swagger UI

Add to `urls.py`:
```python
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(title='Getting Started Winter API', default_version='v1'),
    patterns=urlpatterns,
)
urlpatterns += [
    re_path(r'^$', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
]
```

Add to `settings.py`:
```python
SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'winter_openapi.SwaggerAutoSchema',
}
```

Add `drf_yasg` to `INSTALLED_APPS`:

How to run
----------

Dev server:
```shell
$ poetry run python manage.py runserver
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
1. First create a Heroku application and basic configuration required for python

```shell
$ heroku apps:create winter-getting-started
```

2. Add poetry buildpack for Heroku:
```shell
$ heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
$ heroku buildpacks:add heroku/python
```

3. Add `Procfile` with contents:
```
web: gunicorn simple_api.wsgi
```

4. Disable Django collectstatic since we don't need it

```shell
$ heroku config:set DISABLE_COLLECTSTATIC=1
```

5. Add heroku hosts to settings.ALLOWED_HOSTS
```
ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']
```

6. Then push the current version to deploy it

```shell
$ git push heroku master
```

7. Check it's working https://winter-getting-started.herokuapp.com/greeting/
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
