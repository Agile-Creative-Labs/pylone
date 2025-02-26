class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Pre-process the request
        print("Middleware: Pre-processing request")
        response = self.app(environ, start_response)
        # Post-process the response
        print("Middleware: Post-processing response")
        return response
