from http import HTTPStatus

import winter.web


@winter.web.problem(status=HTTPStatus.BAD_REQUEST)
class NameTooLongException(Exception):
    def __init__(self, max_length: int):
        super().__init__(f'Name must be at most {max_length} characters long')


class SimpleAPI:
    @winter.web.route_get('greeting/')
    def greeting(self) -> str:
        return 'Hello from Winter API!'

    @winter.web.route_get('greeting/{name}/')
    @winter.web.raises(NameTooLongException)
    def personal_greeting(self, name: str) -> str:
        if len(name) > 20:
            raise NameTooLongException(max_length=20)
        return f'Hello, {name}!'
