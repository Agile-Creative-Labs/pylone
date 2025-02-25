from pylone.router import Router
class App:
    def __init__(self, router=None):
        self.router = router or Router()


    def setup(self, router):
        """Sets up the application with a router."""
        self.router = router

    def handle_request(self, environ):
        """Handles incoming HTTP requests."""
        request_path = environ['PATH_INFO']
        request_method = environ['REQUEST_METHOD']
        response = self.router.resolve(request_path, request_method, environ)

        return response.to_wsgi()


