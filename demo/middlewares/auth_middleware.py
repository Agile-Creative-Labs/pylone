"""
   
    Added a list of allowed paths that do not require authentication,
    Improved session handling to avoid errors,
    Added logging for better debugging.

"""

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
        # List of paths that do not require authentication
        self.allowed_paths = [
            "/login",
            "/register",
            "/demo",
            "/ajax-demo",
            "/ajax/data",
            "/test-json",
            "/test-response-object",
            "/test-raw-tuple",
            "/test-json-response",
            "/test-text-response",
            "/test-invalid-response",
            "/test-raw-bytes",
        ]

    def __call__(self, environ, start_response):
        """
        Middleware interface: makes the middleware callable.

        Args:
            environ: The WSGI environment dictionary.
            start_response: The WSGI start_response function.

        Returns:
            The response body as an iterable.
        """
        path = environ["PATH_INFO"]
        logging.debug(f"AuthMiddleware: Checking access for path -> {path}")

        # Skip authentication for allowed paths
        if path in self.allowed_paths:
            logging.debug(f"AuthMiddleware: Allowing access to path -> {path}")
            return self.app(environ, start_response)

        # Check if the user is authenticated
        cookies = environ.get("HTTP_COOKIE", "")
        session_id = None

        # Extract session_id from cookies
        if "session_id=" in cookies:
            session_id = cookies.split("session_id=")[-1].split(";")[0]

        session = session_manager.get_session(session_id) if session_id else None

        if not session:
            # Redirect to login if not authenticated
            logging.debug(f"AuthMiddleware: Redirecting to login -> {path}")
            start_response("302 Found", [("Location", "/login")])
            return [b"Redirecting to login..."]

        # User is authenticated, proceed to the next middleware or app
        logging.debug(f"AuthMiddleware: Allowing access for authenticated user -> {path}")
        return self.app(environ, start_response)
