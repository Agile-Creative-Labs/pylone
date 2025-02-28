import os
import mimetypes
from http import HTTPStatus
from wsgiref.util import FileWrapper
import time
import logging

class StaticFileMiddleware:
    """
    Middleware to serve static files from the specified directory.

    This middleware checks if the incoming request is for a static file.
    If the file exists, it serves the file with the correct MIME type.
    Otherwise, it returns a 404 response.

    Attributes:
        app (callable): The next WSGI application or middleware in the chain.
        static_dir (str): The directory containing static files.
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

        # Serve only requests starting with `/static/`
        if path.startswith("/static/"):
            # Resolve the requested file path safely
            requested_file = os.path.normpath(os.path.join(self.static_dir, path[len("/static/"):]))
            
            # Ensure the requested file is inside the static directory (prevents directory traversal attacks)
            if not requested_file.startswith(self.static_dir):
                start_response(f"{HTTPStatus.FORBIDDEN.value} {HTTPStatus.FORBIDDEN.phrase}", [("Content-Type", "text/plain")])
                return [b"403 Forbidden"]

            # Check if file exists and is a file
            if os.path.exists(requested_file) and os.path.isfile(requested_file):
                return self.serve_static_file(requested_file, start_response)

            # File not found
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

            # Use wsgi.file_wrapper if available for efficient file serving
            return FileWrapper(open(file_path, "rb"), 8192)

        except Exception as e:
            logging.error(f"StaticFileMiddleware -> Error serving {file_path}: {e}")

            start_response(f"{HTTPStatus.INTERNAL_SERVER_ERROR.value} {HTTPStatus.INTERNAL_SERVER_ERROR.phrase}", 
                           [("Content-Type", "text/plain")])
            return [b"500 Internal Server Error"]
