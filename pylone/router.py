# pylone/router.py
from pylone.request import Request
from pylone.response import Response

class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, handler, methods=["GET"]):
        """Registers a route with a handler."""
        self.routes[path] = {"handler": handler, "methods": methods}

    def resolve(self, path, method, environ):
        """Resolves a request to the appropriate handler."""
        if path in self.routes and method in self.routes[path]['methods']:
            return self.routes[path]['handler'](Request(environ))
        return Response("404 Not Found", status=404)
