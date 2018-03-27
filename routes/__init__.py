from collections import UserDict


class RouteTable(UserDict):
    @staticmethod
    def error(request, code=404):
        e = {
            404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
        }
        return e.get(code, b'')

    def route(self, path):
        def decorator(f):
            self[path] = f
            return f

        return decorator

    def handle(self, request):
        path = request.path
        handler = self.get(path, self.error)
        return handler(request)


router = RouteTable()
from routes import (routes_todo, routes_static, routes_user)
