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
