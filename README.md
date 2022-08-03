How to start project with Winter
--------------------------------
1. Bootstrap empty project
```shell
poetry init
poetry add winter
poetry run django-admin startproject simple_api .
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

4. Modify `urls.py` to the following:
```python
from winter_django.autodiscovery import create_django_urls_for_package
from winter.core import set_injector
from injector import Injector

set_injector(Injector())

urlpatterns = [
    *create_django_urls_for_package('simple_api'),
]
```

How to run
----------

Dev server:
```
poetry run python manage.py runserver
```

Manually check it's working
---------------------------

`> http get http://localhost:8000/greeting/`

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

`heroku apps:create winter-getting-started`

2. Add poetry buildpack for Heroku:
```
heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
heroku buildpacks:add heroku/python
```

3. Then push the current version to deploy it

`git push heroku master`
