""" pylone/router.py 


This module implements a Router class for handling HTTP requests and routing them
to appropriate handlers. It supports dynamic route parameters, static file serving,
and method-based routing.

Key features:
    - Route registration with dynamic parameter handling using regular expressions.
    - Method-based routing (e.g., GET, POST).
    - Static file serving from a specified directory.
    - MIME type detection for static files.
    - Error handling and logging.

Usage:
    Initialize a Router instance:
    >>> router = Router()

    Add a route with a handler:
    >>> def my_handler(request, param1, param2):
    ...     return Response(f"Params: {param1}, {param2}")
    >>> router.add_route("/path/<param1>/<param2>", my_handler)

    Resolve a request:
    >>> request = Request("GET", "/path/value1/value2")
    >>> response = router.resolve(request)

    Serve static files:
    Place static files in the 'demo/static' directory, and access them via '/static/'.

Example Static File URLs
/static/css/style.css → Serves demo/static/css/style.css
/static/js/app.js → Serves demo/static/js/app.js
/static/images/logo.png → Serves demo/static/images/logo.png

    Date Created: February 26, 2025
    Author: alex@agilecreativelabs.ca
    Copyright: © 2025 Agile Creative Labs Inc.
"""

import re
import os
import logging
from pylone.response import Response

logging.basicConfig(level=logging.DEBUG)

class Router:
    STATIC_DIR = "demo/static"  # Path to the static directory

    MIME_TYPES = {
        ".html": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".ico": "image/x-icon",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".ttf": "font/ttf",
        ".otf": "font/otf",
        ".eot": "application/vnd.ms-fontobject",
        ".json": "application/json",
        ".txt": "text/plain"
    }

    def __init__(self):
        """Initialize the router with an empty routes dictionary."""
        self.routes = {}

    def add_route(self, path, handler, methods=["GET"]):
        """
        Register a route with a handler.

        Args:
            path (str): The URL path for the route.
            handler (function): The function to handle the request.
            methods (list): List of HTTP methods allowed for the route (e.g., ["GET", "POST"]).
        """
        # Convert dynamic route parameters to a regex pattern
        pattern = re.sub(r"<(\w+:)?(\w+)>", r"(?P<\2>[^/]+)", path)
        self.routes[path] = {"pattern": re.compile(f"^{pattern}$"), "handler": handler, "methods": methods}
        logging.debug(f"ROUTER Route added-> {path} with methods {methods}")

    def resolve(self, request):
        """
        Resolve a request to the appropriate handler.

        Args:
            request (Request): The request object containing path and method.

        Returns:
            Response: A response object to send back to the client.
        """
        path = request.path
        method = request.method
        logging.debug(f"ROUTER Resolving request-> {method} {path}")

        # Serve static files if the request is for /static/*
        if path.startswith("/static/"):
            return self.serve_static_file(path)

        # Check if the path matches any route
        for route_path, route in self.routes.items():
            match = route["pattern"].match(path)
            if match:
                logging.debug(f"ROUTER Route found -> {route_path}")
                # Check if the request method is allowed for the route
                if method in route["methods"]:
                    logging.debug(f"Method {method} allowed for {route_path}")
                    handler = route["handler"]
                    # Pass dynamic parameters to the handler
                    kwargs = match.groupdict()
                    response = handler(request, **kwargs)  # Call the handler
                    if response is None:
                        logging.error(f"ROUTER Handler for {route_path} returned None")
                        return Response("ROUTER 500 Internal Server Error", status=500)
                    return response  # Return the response
                else:
                    # Method not allowed
                    logging.warning(f"ROUTER Method {method} not allowed for {route_path}")
                    return Response("ROUTER 405 Method Not Allowed", status=405)

        # Route not found
        logging.warning(f"ROUTER 404 Not Found: {method} {path}")
        return Response("ROUTER 404 Not Found", status=404)

    def serve_static_file(self, path):
        """
        Serve a static file from the static directory.

        Args:
            path (str): The request path starting with /static/

        Returns:
            Response: A response containing the file content or a 404 error.
        """
        file_path = os.path.join(self.STATIC_DIR, path.lstrip("/"))  # Remove leading "/"

        if os.path.exists(file_path) and os.path.isfile(file_path):
            _, ext = os.path.splitext(file_path)
            content_type = self.MIME_TYPES.get(ext, "application/octet-stream")

            try:
                with open(file_path, "rb") as file:
                    content = file.read()
                logging.debug(f"STATIC FILE SERVED: {file_path}")
                return Response(content, status=200, content_type=content_type)
            except Exception as e:
                logging.error(f"STATIC FILE ERROR: Unable to read {file_path}: {e}")
                return Response("ROUTER 500 Internal Server Error", status=500)

        logging.warning(f"STATIC FILE NOT FOUND: {file_path}")
        return Response("ROUTER 404 Not Found", status=404)
