"""
Test Controller for Pylone Web Framework.

This module provides the TestController class, which is used to test various
response types and scenarios within the Pylone web framework. It demonstrates
how to return different types of responses, including Response objects,
raw tuples, JSON responses, plain text responses, raw bytes responses, and
invalid responses.

Imports:
    demo.database.db: The database instance from the demo application (not used in this module).
    pylone.response.Response: The response object for creating HTTP responses (not directly used in all methods).
    pylone.session.session_manager: The session manager for handling user sessions (not used in this module).
    pylone.template.TemplateEngine: The template engine for rendering HTML templates (not used in this module).
    logging: For logging messages.
    os: For interacting with the operating system (e.g., file paths) (not used in this module).
    json: For encoding and decoding JSON data (not directly used in all methods).

Classes:
    TestController: Handles various test response scenarios.

Functions:
    None.

 Author: Agile Creative Labs Inc.
 Version: 1.0.0
 Date: 02/23/2024
"""
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
    
    def links(self, request):
        """Demo links."""
        logging.debug("TestController: Demo links")
        return Response(template_engine.render("public/links.html", {}), status=200)