# controllers/chat_controller.py
from demo.database import db
from pylone.response import Response
from pylone.session import session_manager
from pylone.template import TemplateEngine
import logging
import os
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize TemplateEngine with the templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../templates/")
template_engine = TemplateEngine(TEMPLATES_DIR)

class ChatController:
    def index(self, request):
        """Serve the chat interface."""
        logging.debug("ChatController: Serving chat interface")
        
        # Get user from session if authenticated
        #user_id = session_manager.get(request, 'user_id')
        #username = None
        
        #if user_id:
        #    user = db.get_user_by_id(user_id)
        #    if user:
        #        username = user[1]  # Assuming username is at index 1
        
        # Pass data to template
        context = {
            'username': 'Cooper',
            'ws_url': f"ws://{request.get_host().split(':')[0]}:8001/chat"  # Assuming WebSocket runs on port 8001
        }
        
        return Response(template_engine.render("private/chatbot.html", context), status=200)
    
    def get_messages(self, request):
        """API endpoint to get recent messages."""
        logging.debug("ChatController: Getting recent messages")
        
        # You would implement this to fetch recent messages from your database
        # For example:
        # messages = db.get_recent_messages(10)  # Get last 10 messages
        
        # For now, return a placeholder
        messages = [
            {"username": "System", "message": "Welcome to the chat!", "timestamp": "2023-01-01T00:00:00"}
        ]
        
        return Response(json.dumps({"messages": messages}), status=200, content_type="application/json")
    
    def auth_required(self, request):
        """Return whether authentication is required for chat."""
        auth_required = True  # You can make this dynamic based on your app config
        
        return Response(json.dumps({"auth_required": auth_required}), 
                       status=200, 
                       content_type="application/json")