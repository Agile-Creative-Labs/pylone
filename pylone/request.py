import logging

class Request:
    def __init__(self, environ):
        self.environ = environ
        self.method = environ['REQUEST_METHOD']
        self.path = environ['PATH_INFO']
        self.headers = environ.get('HTTP_HEADERS', {})
        self.cookies = self._parse_cookies(environ.get('HTTP_COOKIE', ''))
        self.form_data = self._parse_form_data(environ)
        logging.debug(f"Request Path Extracted: {self.path}")

    def get(self, key, default=None):
        """Retrieve a value from the form data."""
        return self.form_data.get(key, default)

    def _parse_cookies(self, cookie_header):
        """Parse cookies from the HTTP_COOKIE header."""
        cookies = {}
        if cookie_header:
            for cookie in cookie_header.split(';'):
                key, value = cookie.strip().split('=', 1)
                cookies[key] = value
        return cookies

    def _parse_form_data(self, environ):
        """Parse form data from the request."""
        form_data = {}
        if environ['REQUEST_METHOD'] == 'POST':
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except ValueError:
                request_body_size = 0

            if request_body_size > 0:
                request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
                for pair in request_body.split('&'):
                    key, value = pair.split('=')
                    form_data[key] = value
        return form_data