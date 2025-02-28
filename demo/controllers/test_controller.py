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
        return "200 OK", [("Content-Type", "text/plain")], [b"Hello, World!"]

    def test_response_object(request):
        return MyResponse()

    def test_raw_tuple(request):
        return "Hello, World!", 200, {"Content-Type": "text/plain"}
    
    def test_json_response(request):
        return {"message": "Hello, World!", "status": "success"}    

    def test_text_response(request):
        return "Hello, World!"
    
    def test_invalid_response(request):
        return None