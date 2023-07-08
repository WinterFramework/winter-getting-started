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
