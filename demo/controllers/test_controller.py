from demo.database import db  # Import the database instance
from pylone.response import Response
from pylone.session import session_manager
from pylone.template import TemplateEngine  # Import the template engine
import logging
import os
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize TemplateEngine with the templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../templates/")
template_engine = TemplateEngine(TEMPLATES_DIR)

class TestController:
    def to_wsgi(self):
        """Simulate a Response object with a to_wsgi method."""
        return "200 OK", [("Content-Type", "text/plain")], [b"Hello, World!"]

    def test_response_object(self, request):
        """Test a Response object with a to_wsgi method."""
        logging.debug("TestController: Returning Response object")
        return self  # Return the TestController instance, which has a to_wsgi method

    def test_raw_tuple(self, request):
        """Test a raw tuple (body, status, headers)."""
        logging.debug("TestController: Returning raw tuple")
        return "Hello, World!", 200, {"Content-Type": "text/plain"}

    def test_json_response(self, request):
        """Test a JSON response (dictionary)."""
        logging.debug("TestController: Returning JSON response")
        return {"message": "Hello, World!", "status": "success"}

    def test_text_response(self, request):
        """Test a plain text response (string)."""
        logging.debug("TestController: Returning plain text response")
        return "Hello, World!"

    def test_raw_bytes_response(self, request):
        """Test a raw bytes response."""
        logging.debug("TestController: Returning raw bytes response")
        return b"Raw bytes response"

    def test_invalid_response(self, request):
        """Test an invalid response (None)."""
        logging.debug("TestController: Returning invalid response")
        return None