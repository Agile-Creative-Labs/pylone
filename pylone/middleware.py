class Middleware:
    def __init__(self, app):
        """
        Initialize the middleware with the WSGI application.

        Args:
            app: The WSGI application to wrap.
        """
        self.app = app

    def __call__(self, environ, start_response):
        """
        Middleware interface: makes the middleware callable.

        Args:
            environ: The WSGI environment dictionary.
            start_response: The WSGI start_response function.

        Returns:
            The response body as an iterable.
        """
        # Pre-process the request
        self.pre_process(environ)

        # Call the next middleware or the app
        response = self.app(environ, start_response)

        # Post-process the response
        self.post_process(environ, response)

        return response

    def pre_process(self, environ):
        """
        Pre-process the request (e.g., logging, authentication).

        Args:
            environ: The WSGI environment dictionary.
        """
        logging.debug(f"Middleware: Pre-processing request for {environ['PATH_INFO']}")

    def post_process(self, environ, response):
        """
        Post-process the response (e.g., logging, adding headers).

        Args:
            environ: The WSGI environment dictionary.
            response: The WSGI response.
        """
        logging.debug(f"Middleware: Post-processing response for {environ['PATH_INFO']}")