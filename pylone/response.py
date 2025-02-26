import logging
# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Response:
    def __init__(self, body, status=200, headers=None, cookies=None):
        self.body = body
        self.status = f"{status} OK" if isinstance(status, int) else status
        self.headers = list(headers) if headers is not None else []  # Ensure headers is a list
        self.cookies = cookies if cookies is not None else {}

    def to_wsgi(self):
        """Convert the response to a WSGI-compatible format."""
        # Ensure headers is a list of tuples
        headers = self.headers.copy()

        # Add cookies to headers
        for key, value in self.cookies.items():
            headers.append(("Set-Cookie", f"{key}={value}; Path=/"))

        # Log headers and cookies
        logging.debug(f"Response headers: {headers}")
        logging.debug(f"Response cookies: {self.cookies}")

        # Ensure body is an iterable (e.g., a list of bytes)
        body = [self.body.encode('utf-8')] if isinstance(self.body, str) else self.body
        return self.status, headers, body