from pylone.router import Router
from pylone.request import Request
from pylone.middleware import Middleware
import logging
class App:
    def __init__(self, router=None, middlewares=None):
        """
        Initialize the application with a router and middlewares.

        Args:
            router: The router to use for resolving requests.
            middlewares: A list of middleware classes to apply.
        """
        self.router = router or Router()
        self.middlewares = middlewares or []

    def setup(self, router):
        """Set up the application with a router."""
        self.router = router

    def handle_request(self, environ, start_response):
        """
        Handle an incoming HTTP request.

        Args:
            environ: The WSGI environment dictionary.
            start_response: The WSGI start_response function.

        Returns:
            The response body as an iterable.
        """
        request = Request(environ)  # Create a Request object
        response = self.router.resolve(request)  # Resolve the request
        status, headers, body = response.to_wsgi()  # Convert response to WSGI format
        start_response(status, headers)  # Start the WSGI response
        return body  # Return the response body

    def __call__(self, environ, start_response):
        """WSGI interface: makes the App instance callable."""
        # Apply middlewares in reverse order (last added is first executed)
        app = self.handle_request
        for middleware in reversed(self.middlewares):
            app = middleware(app)

        # Call the wrapped app
        return app(environ, start_response)