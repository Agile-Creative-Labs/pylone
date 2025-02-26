from pylone.router import Router
from pylone.request import Request
import logging
class App:
    def __init__(self, router=None):
        self.router = router or Router()

    def setup(self, router):
        """Sets up the application with a router."""
        self.router = router

    def handle_request(self, environ):
        """Handles incoming HTTP requests."""
        request = Request(environ)  # Create a Request object
        response = self.router.resolve(request)  # Resolve the request
        if response is None:
            logging.error("Router returned None")
            response = Response("500 Internal Server Error", status=500)
        return response.to_wsgi()  # Convert response to WSGI format

    def __call__(self, environ, start_response):
        """WSGI interface: makes the App instance callable."""
        status, headers, body = self.handle_request(environ)  # Handle the request
        start_response(status, headers)  # Start the WSGI response
        return body  # Return the response body