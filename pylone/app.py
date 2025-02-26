from pylone.router import Router
from pylone.request import Request

class App:
    def __init__(self, router=None):
        self.router = router or Router()

    def setup(self, router):
        """Sets up the application with a router."""
        self.router = router

    def handle_request(self, environ):
        """Handles incoming HTTP requests."""
        request = Request(environ)  # Create a Request object
        response = self.router.resolve(request.path, request.method)  # Only pass path and method

        return response.to_wsgi()  # Convert response to WSGI format




