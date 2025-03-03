"""pylone/response.py

This module defines the Response class, which encapsulates HTTP responses for
a WSGI application. It handles various response body types, status codes,
headers, and cookies, and provides a method to convert the response to a
WSGI-compatible format.

Key features:
    - Initialization with body, status, headers, and cookies.
    - Automatic status message generation from status code.
    - Cookie handling and inclusion in headers.
    - JSON serialization for dictionary bodies.
    - String encoding for HTML or plain text bodies.
    - Support for iterable byte bodies.
    - Logging of response details.
    - Conversion to WSGI-compatible (status, headers, body) tuple.

Usage:
    Create a Response object:
    >>> response = Response("Hello, World!", status=200, headers={"Content-Type": "text/plain"})

    Create a JSON response:
    >>> response = Response({"message": "Success"}, status=200)

    Create a response with cookies:
    >>> response = Response("Cookie set!", status=200, cookies={"session_id": "12345"})

    Convert to WSGI format:
    >>> status, headers, body = response.to_wsgi()

    Date Created: February 26, 2025
    Author: alex@agilecreativelabs.ca
    Copyright: © 2025 Agile Creative Labs Inc.
"""
import logging
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Response:
    STATUS_MESSAGES = {
        200: "OK",
        201: "Created",
        400: "Bad Request",
        404: "Not Found",
        500: "Internal Server Error",
    }

    def __init__(self, body, status=200, headers=None, cookies=None):
        """
        Initialize a Response object.

        Args:
            body: The response body (str, dict, or iterable of bytes).
            status: The HTTP status code (int or str).
            headers: A dictionary or list of tuples representing HTTP headers.
            cookies: A dictionary of cookies to set in the response.
        """
        self.body = body
        self.status = f"{status} {self.STATUS_MESSAGES.get(status, 'Unknown')}" if isinstance(status, int) else status
        self.headers = list(headers.items()) if isinstance(headers, dict) else list(headers or [])
        self.cookies = cookies if cookies is not None else {}

    def to_wsgi(self):
        """Convert the response to a WSGI-compatible format."""
        # Ensure headers is a list of tuples
        headers = self.headers.copy()

        # Add cookies to headers
        for key, value in self.cookies.items():
            cookie_value = f"{key}={value}; Path=/"
            if hasattr(value, 'path'):
                cookie_value += f"; Path={value.path}"
            headers.append(("Set-Cookie", cookie_value))

        # Log response details
        logging.debug(f"Response status: {self.status}")
        logging.debug(f"Response headers: {headers}")
        logging.debug(f"Response cookies: {self.cookies}")

        # Handle body encoding
        if isinstance(self.body, dict):
            # Serialize JSON data
            body = [json.dumps(self.body).encode('utf-8')]
            headers.append(("Content-Type", "application/json"))
        elif isinstance(self.body, str):
            # Encode HTML or plain text
            body = [self.body.encode('utf-8')]
            headers.append(("Content-Type", "text/html"))
        else:
            # Assume body is already an iterable of bytes
            body = [chunk.encode('utf-8') if isinstance(chunk, str) else chunk for chunk in self.body]

        return self.status, headers, body