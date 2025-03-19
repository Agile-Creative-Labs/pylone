"""
Logging Middleware for a Python WSGI Application.

This module provides a middleware class, LoggingMiddleware, that wraps a WSGI
application to log incoming requests and outgoing responses. It logs the request
method and path, as well as the response status. In case of critical errors, it
logs the error and forcefully terminates the program.

Imports:
    logging: For logging messages.
    sys: For system-specific parameters and functions (not directly used here, but potentially needed for more advanced logging).
    os: For operating system interfaces, used here to forcefully terminate the program on critical errors.

Classes:
    LoggingMiddleware: A WSGI middleware that logs requests and responses.

Functions:
    None.
    
 Author: Agile Creative Labs Inc.
 Version: 1.0.0
 Date: 02/23/2024
"""
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

            