class Response:
    def __init__(self, body, status=200, headers=None):
        self.body = body
        self.status = f"{status} OK" if isinstance(status, int) else status  # Convert int to str
        self.headers = headers or [("Content-Type", "text/html")]

    def to_wsgi(self):
        """Convert the response to a WSGI-compatible format."""
        # Ensure headers are a list of tuples
        headers = self.headers if isinstance(self.headers, list) else list(self.headers.items())
        # Ensure body is an iterable (e.g., a list of bytes)
        body = [self.body.encode('utf-8')] if isinstance(self.body, str) else self.body
        return self.status, headers, body