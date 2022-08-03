import winter


@winter.web.no_authentication
class SimpleAPI:
    @winter.route_get('greeting/')
    def greeting(self) -> str:
        return 'Hello from Winter API!'
