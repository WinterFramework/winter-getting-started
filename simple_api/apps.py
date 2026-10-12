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
