from django.http import HttpResponse

import winter
import winter_openapi


@winter.web.no_authentication
class SwaggerUI:
    @winter.route_get('')
    def get_swagger_ui(self):
        html = winter_openapi.get_swagger_ui_html(openapi_url='/openapi?format=openapi')
        return HttpResponse(html, content_type='text/html')
