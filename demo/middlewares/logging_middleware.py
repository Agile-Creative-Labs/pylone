import logging
import sys
import os

class LoggingMiddleware:
    def __init__(self, app):
        """
        Initialize the logging middleware.

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
        try:
            # Log the request
            logging.info(f"LoggingMiddleware REQUEST -> {environ['REQUEST_METHOD']} {environ['PATH_INFO']}")

            # Call the next middleware or the app
            def custom_start_response(status, headers, exc_info=None):
                # Log the response status
                logging.info(f"LoggingMiddleware RESPOMSE -> {status}")
                return start_response(status, headers, exc_info)

            response = self.app(environ, custom_start_response)

            return response
        except Exception as e:
            logging.error(f"LoggingMiddleware Critical error -> {e}")
            os._exit(1)  # Forcefully terminate the program