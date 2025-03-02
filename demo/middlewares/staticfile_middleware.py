"""
demo/staticfile_middleware.py
    Middleware for serving static files in a WSGI application.
        This middleware intercepts requests for static files (e.g., CSS, JS, images) and serves them
    directly from a specified directory. It handles file existence checks, MIME type detection,
    and proper HTTP headers for caching and security.
# Author: alex@agilecreativelabs.ca
# Date: Thu Feb 27, 2025
# Copyright: Copyright (c) 2025 Agile Creative Labs Inc
"""
import os
import mimetypes
from http import HTTPStatus
from wsgiref.util import FileWrapper
import time
import logging

class StaticFileMiddleware:
    """
    Middleware for serving static files in a WSGI application.

    This middleware intercepts requests for static files (e.g., CSS, JS, images) and serves them
    directly from a specified directory. It handles file existence checks, MIME type detection,
    and proper HTTP headers for caching and security.

    Attributes:
        app (callable): The next WSGI application or middleware in the chain.
        static_dir (str): The absolute path to the directory containing static files.

    Methods:
        __call__(environ, start_response): Intercepts WSGI requests and serves static files if applicable.
        serve_static_file(file_path, start_response): Serves a static file with proper headers and error handling.

    Example:
        To use this middleware, wrap your WSGI application as follows:
        ```
        app = StaticFileMiddleware(your_wsgi_app, static_dir="/path/to/static")
        ```

    Notes:
        - Static files are served under the `/static/` URL prefix.
        - Files outside the `static_dir` are blocked to prevent directory traversal attacks.
        - Supports caching via the `Cache-Control` header.
        - Returns appropriate HTTP status codes (200, 403, 404, 500) for different scenarios.
    """

    def __init__(self, app, static_dir='static'):
        """
        Initialize the StaticFileMiddleware.

        Args:
            app (callable): The next WSGI application or middleware.
            static_dir (str, optional): The directory for static files. Defaults to 'static'.
        """
        self.app = app
        self.static_dir = os.path.abspath(static_dir)  # Ensure absolute path
        logging.info(f"StaticFileMiddleware -> Static directory: {self.static_dir}")
        mimetypes.init()  # Initialize MIME types

    def __call__(self, environ, start_response):
        """
        Process incoming WSGI requests and serve static files if applicable.

        Args:
            environ (dict): The WSGI environment dictionary.
            start_response (callable): The WSGI start_response function.

        Returns:
            iterable: The response body as an iterable of bytes.
        """
        path = environ.get("PATH_INFO", "")
        logging.info(f"StaticFileMiddleware -> Requested path: {path}")
        # Serve only requests starting with `/static/`
        if path.startswith("/static/"):
            relative_path = path[len("/static/"):]
            logging.info(f"StaticFileMiddleware -> Relative path: {relative_path}")
            # Resolve the requested file path safely
            requested_file = os.path.normpath(os.path.join(self.static_dir, relative_path))
            logging.info(f"StaticFileMiddleware -> Resolved file: {requested_file}")  # Add this line
            # Ensure the requested file is inside the static directory (prevents directory traversal attacks)
            if not requested_file.startswith(self.static_dir):
                start_response(f"{HTTPStatus.FORBIDDEN.value} {HTTPStatus.FORBIDDEN.phrase}", [("Content-Type", "text/plain")])
                return [b"403 Forbidden"]

            # Check if file exists and is a file
            if os.path.exists(requested_file) and os.path.isfile(requested_file):
                logging.info(f"StaticFileMiddleware -> File exists: {requested_file}")
                return self.serve_static_file(requested_file, start_response)

            # File not found
            logging.error(f"StaticFileMiddleware -> File not found: {requested_file}")
            start_response(f"{HTTPStatus.NOT_FOUND.value} {HTTPStatus.NOT_FOUND.phrase}", [("Content-Type", "text/plain")])
            return [b"404 File Not Found"]

        # Pass to the next middleware or app
        return self.app(environ, start_response)

    def serve_static_file(self, file_path, start_response):
        """
        Serve the requested static file efficiently.

        Args:
            file_path (str): The absolute path of the static file to be served.
            start_response (callable): The WSGI start_response function.

        Returns:
            iterable: The file content as an iterable of bytes.
        """
        try:
            file_size = os.path.getsize(file_path)
            last_modified = time.gmtime(os.path.getmtime(file_path))  # Get last modified time

            # Determine MIME type
            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type = mime_type or "application/octet-stream"

            # Prepare headers
            headers = [
                ("Content-Type", mime_type),
                ("Content-Length", str(file_size)),
                ("Cache-Control", "public, max-age=86400"),  # Cache for 1 day
                ("Last-Modified", time.strftime("%a, %d %b %Y %H:%M:%S GMT", last_modified)),
            ]

            # Start WSGI response
            start_response(f"{HTTPStatus.OK.value} {HTTPStatus.OK.phrase}", headers)

            # Read the file content and return it as an iterable
            with open(file_path, "rb") as file:
                return [file.read()]  # Return the file content as a list of bytes

        except Exception as e:
            logging.error(f"StaticFileMiddleware -> Error serving {file_path}: {e}")

            start_response(f"{HTTPStatus.INTERNAL_SERVER_ERROR.value} {HTTPStatus.INTERNAL_SERVER_ERROR.phrase}", 
                       [("Content-Type", "text/plain")])
            return [b"500 Internal Server Error"]