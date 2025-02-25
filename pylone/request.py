# pylone/request.py
class Request:
    def __init__(self, environ):
        self.environ = environ
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.headers = environ.get('HTTP_HEADERS', {})

    def get(self, key, default=None):
        return self.environ.get(key, default)
