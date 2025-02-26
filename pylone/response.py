class Response:
    def __init__(self, body, status=200, headers=None):
        self.body = body
        self.status = f"{status} OK" if isinstance(status, int) else status  # Convert int to str
        self.headers = headers or [("Content-Type", "text/html")]

    def to_wsgi(self):
        """Convert the response to a WSGI-compatible format."""
        self.headers['Content-Type'] = 'text/html; charset=utf-8'
        return self.status, list(self.headers.items()), [self.body.encode('utf-8')]

