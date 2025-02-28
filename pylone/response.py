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