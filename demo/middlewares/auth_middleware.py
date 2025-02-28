from pylone.session import session_manager
import logging

class AuthMiddleware:
    def __init__(self, app):
        """
        Initialize the authentication middleware.

        Args:
            app: The WSGI application to wrap.
        """
        self.app = app

    def __call__(self, environ, start_response):
        """
        Middleware interface: makes the middleware callable.

        Args:
            environ: The WSGI environment dictionary.
            start_response: The WSGI start_response function.

        Returns:
            The response body as an iterable.
        """
        # Check if the user is authenticated
        session_id = environ.get("HTTP_COOKIE", "").split("session_id=")[-1].split(";")[0]
        session = session_manager.get_session(session_id)

        if not session and environ["PATH_INFO"] not in ["/login", "/register", "/demo"]:
            # Redirect to login if not authenticated
            start_response("302 Found", [("Location", "/login")])
            return [b"Redirecting to login..."]

        # Call the next middleware or the app
        return self.app(environ, start_response)