# pylone/response.py
class Response:
    def __init__(self, body, status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {}

    def to_wsgi(self):
        """Convert the response to a WSGI-compatible format."""
        self.headers['Content-Type'] = 'text/html; charset=utf-8'
        return self.status, list(self.headers.items()), [self.body.encode('utf-8')]
