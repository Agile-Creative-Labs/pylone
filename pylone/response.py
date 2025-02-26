class Response:
    def __init__(self, body, status=200, headers=None, cookies=None):
        self.body = body
        self.status = f"{status} OK" if isinstance(status, int) else status
        self.headers = headers or [("Content-Type", "text/html")]
        self.cookies = cookies or {}

    def to_wsgi(self):
        """Convert the response to a WSGI-compatible format."""
        # Add cookies to headers
        headers = self.headers.copy()
        for key, value in self.cookies.items():
            headers.append(("Set-Cookie", f"{key}={value}; Path=/"))

        # Ensure body is an iterable (e.g., a list of bytes)
        body = [self.body.encode('utf-8')] if isinstance(self.body, str) else self.body
        return self.status, headers, body