import winter.django
import winter.web

routes = [
    *winter.web.find_package_routes('simple_api.api'),
    *winter.web.find_package_routes('simple_api.openapi'),
]
urlpatterns = winter.django.create_django_urls_from_routes(routes)
