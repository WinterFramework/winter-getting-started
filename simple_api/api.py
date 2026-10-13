import winter.web


class SimpleAPI:
    @winter.web.route_get('greeting/')
    def greeting(self) -> str:
        return 'Hello from Winter API!'
