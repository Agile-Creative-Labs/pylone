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

class AjaxController:
    def __init__(self):
        """Initialize the AjaxController with a template engine."""
        self.template_engine = template_engine

    def test_json_response(self, request):
        """Test JSON response."""
        logging.debug("AjaxController: Handling /ajax/test-json request")
        try:
            data = {
                'message': 'Test JSON response',
                'status': 'success',
            }
            response = self.json_response(data)
            logging.debug(f"AjaxController: Response -> {response}")
            return response
        except Exception as e:
            logging.error(f"AjaxController: Error in test_json_response -> {e}")
            raise

    def json_response(self, data, status=200):
        """
        Return a JSON response.

        Args:
            data: The data to include in the response.
            status: The HTTP status code (default: 200).

        Returns:
            A tuple containing the JSON response, status code, and headers.
        """
        response = {
            'status': status,
            'data': data,
        }
        return json.dumps(response), status, {'Content-Type': 'application/json'}

    def get_data(self, request):
        """Handle AJAX data requests."""
        logging.debug("AjaxController: Handling /ajax/data request")
        try:
            data = {
                'message': 'Hello from Pylone!',
                'status': 'success',
            }
            response = self.json_response(data)
            logging.debug(f"AjaxController: Response -> {response}")
            return response
        except Exception as e:
            logging.error(f"AjaxController: Error in get_data -> {e}")
            raise

    def ajax_demo(self, request):
        """Render the AJAX demo page."""
        # Render the AJAX demo page with a dynamic title
        context = {
            'title': 'AJAX Demo Page',
        }
        body, status, headers = self.template_engine.render_template('public/ajax_demo.html', context)
        return Response(body, status=status, headers=headers)

ajax_controller = AjaxController()