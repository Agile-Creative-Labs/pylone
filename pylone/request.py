import logging

class Request:
    def __init__(self, environ):
        self.environ = environ
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.headers = environ.get('HTTP_HEADERS', {})
        logging.debug(f"Request Path Extracted: {self.path}")

    def get(self, key, default=None):
        return self.environ.get(key, default)
