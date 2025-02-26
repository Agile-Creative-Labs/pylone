import logging
from pylone.request import Request
from pylone.response import Response

logging.basicConfig(level=logging.DEBUG)

class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, handler, methods=["GET"]):
        """Registers a route with a handler."""
        self.routes[path] = {"handler": handler, "methods": methods}

    def resolve(self, request):
        """Resolves a request to the appropriate handler."""
        path = request.path
        method = request.method
        logging.debug(f"Resolving request: {method} {path}")
        if path in self.routes and method in self.routes[path]['methods']:
            return self.routes[path]['handler'](request)
        logging.warning(f"404 Not Found: {method} {path}")
        return Response("404 Not Found", status=404)

