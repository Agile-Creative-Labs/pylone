class Middleware:
    def __init__(self, app):
        self.app = app
        self.middlewares = []

    def add(self, middleware_func):
        """Adds a middleware function to the stack."""
        self.middlewares.append(middleware_func)

    def process_request(self, environ):
        """Processes a request through all middleware functions."""
        for middleware in self.middlewares:
            environ = middleware(environ)
        return self.app.handle_request(environ)
