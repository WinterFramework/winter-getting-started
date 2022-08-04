import winter.core
import winter_django
import winter_openapi
from injector import Injector


winter.core.set_injector(Injector())
winter.web.setup()
winter_django.setup()
winter_openapi.setup(allow_missing_raises_annotation=True)
