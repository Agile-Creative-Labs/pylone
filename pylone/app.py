import os
import json
import logging
from pylone.router import Router
from pylone.request import Request
from pylone.middleware import Middleware
from pylone.template import TemplateEngine

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../templates/")

class App:
    """
        The main application class for handling HTTP requests in the Pylone MVC framework.
        This class acts as a WSGI application, handling requests, resolving routes, 
        processing responses, and ensuring WSGI-compliant output.
    
    """
    def __init__(self, router=None, middlewares=None, templates_dir=None):
        """
        Initialize the application with a router and middlewares.

        Args:
            router: The router to use for resolving requests.
            middlewares: A list of middleware classes to apply.
            templates_dir: Directory containing templates (defaults to TEMPLATES_DIR).
        """
        self.router = router or Router()
        self.middlewares = middlewares or []
        self.template_engine = TemplateEngine(templates_dir or TEMPLATES_DIR)

    def render_template(self, template_name, context=None, status=200, headers=None):
        """Render a template and return a WSGI-compliant response."""
        return self.template_engine.render_template(template_name, context, status, headers)

    def json_response(self, data, status=200):
        """Return a JSON response."""
        response = {
            'status': status,
            'data': data,
        }
        return json.dumps(response), status, {'Content-Type': 'application/json'}

    def setup(self, router):
        """Set up the application with a router."""
        self.router = router
    
    def handle_request(self, environ, start_response):
        """
        Handle an incoming HTTP request and generate a WSGI-compliant response.

        Args:
            environ (dict): The WSGI environment dictionary containing request metadata.
            start_response (callable): The WSGI start_response function.

        Returns:
            list: An iterable containing the response body as bytes.
        """
        try:
            # Create a Request object
            request = Request(environ)
            
            # Resolve the request via router
            response = self.router.resolve(request)

            # Determine response type and standardize it
            status, headers, body = self.process_response(response)

            # Ensure headers is a list of tuples
            if isinstance(headers, dict):
                headers = list(headers.items())

            # Ensure body is bytes
            if isinstance(body, str):
                body = [body.encode("utf-8")]
            elif isinstance(body, (bytes, bytearray)):
                body = [body]
            elif isinstance(body, list):
                body = [b if isinstance(b, (bytes, bytearray)) else str(b).encode("utf-8") for b in body]
            else:
                body = [b"Internal Server Error"]

            # Start the WSGI response
            start_response(f"{status} OK", headers)
            return body

        except Exception as e:
            logging.error(f"APP -> Critical error handling request: {e}")
            logging.error(traceback.format_exc())  # Log the full traceback
            start_response("500 Internal Server Error", [("Content-Type", "text/plain")])
            return [b"Internal Server Error"]

    def process_response(self, response):
        """
        Process different response types and return standardized values for WSGI.

        Supported response types:
        - Response object with `to_wsgi()`
        - Tuple (body, status, headers)
        - Dictionary (converted to JSON)
        - String (plain text response)
        - Bytes (binary response)
        - Unknown response types return a 500 Internal Server Error.

        Args:
            response (various): The response returned by a controller or middleware.

        Returns:
            tuple: (status_code, headers, body)
                - status_code (int): HTTP status code (e.g., 200, 404, 500).
                - headers (list): A list of (key, value) header tuples.
                - body (str or bytes): The response body.
        """
        if hasattr(response, "to_wsgi"):
            # Case 1: Response object with a to_wsgi() method
            status, headers, body = response.to_wsgi()
        elif isinstance(response, tuple) and len(response) == 3:
            # Case 2: Raw tuple (body, status, headers)
            body, status, headers = response
        elif isinstance(response, dict):
            # Case 3: JSON response
            body = json.dumps(response)
            status = 200
            headers = {"Content-Type": "application/json; charset=utf-8"}
        elif isinstance(response, str):
            # Case 4: Plain text response
            body = response
            status = 200
            headers = {"Content-Type": "text/plain; charset=utf-8"}
        elif isinstance(response, bytes):
            # Case 5: Raw bytes response
            body = response
            status = 200
            headers = {"Content-Type": "application/octet-stream"}
        else:
            # Case 6: Unsupported response type
            body = "Internal Server Error"
            status = 500
            headers = {"Content-Type": "text/plain"}

        return status, headers, body
    
    def _handle_request(self, environ, start_response):
        """
        Handle an incoming HTTP request.

        Args:
            environ: The WSGI environment dictionary.
            start_response: The WSGI start_response function.

        Returns:
            The response body as an iterable.
        """
        try:
            request = Request(environ)  # Create a Request object
            response = self.router.resolve(request)  # Resolve the request
            status, headers, body = response.to_wsgi()  # Convert response to WSGI format
            start_response(status, headers)  # Start the WSGI response
            return body  # Return the response body
        except Exception as e:
            logging.error(f"APP -> Critical error handling request: {e}")
            os._exit(1)  # Forcefully terminate the program

    def __call__(self, environ, start_response):
        """WSGI interface: makes the App instance callable."""
        try:
            # Apply middlewares in reverse order (last added is first executed)
            app = self.handle_request
            for middleware in reversed(self.middlewares):
                app = middleware(app)

            # Call the wrapped app
            return app(environ, start_response)
        except Exception as e:
            logging.error(f"APP -> Critical error in middleware or app: {e} Exiting Pylone ...")
            os._exit(1)  # Forcefully terminate the program