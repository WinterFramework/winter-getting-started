import winter_openapi

swagger_ui_route = winter_openapi.create_swagger_ui_route(
    openapi_url='/openapi?format=openapi',
    title='Handmade Swagger UI',
    url='',
)
