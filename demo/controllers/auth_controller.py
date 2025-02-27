"""
demo/controllers/auth_controller.py

@TODO: 
instead of dynamically generating the html tags use the template engine and the html files from /demo/templates/ 
for both methods login and register
"""

from demo.database import db  # Import the database instance
from pylone.response import Response
from pylone.session import session_manager
from pylone.template import TemplateEngine  # Import the template engine
import logging
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize TemplateEngine with the templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../templates/")
template_engine = TemplateEngine(TEMPLATES_DIR)

class AuthController:
    def login(self, request):
        """Handles the login page."""
        if request.method == "POST":
            username = request.get("username")
            password = request.get("password")
            user = db.get_user(username)  # Fetch user from DB

            if user and user[2] == password:  # Check if password matches
                # Create a session for the user
                session_id = session_manager.create_session(user[0])  # user[0] is the user ID
                # Redirect to the dashboard with a session cookie
                return Response(
                    "",
                    status=302,
                    headers=[("Location", "/dashboard")],
                    cookies={"session_id": session_id}
                )
            else:
                # Re-render login page with an error message
                context = {"error": "Invalid username or password."}
                return Response(template_engine.render("login.html", context), status=401)
        
        # Render login form
        return Response(template_engine.render("login.html"))

    def register(self, request):
        """Handles the registration page."""
        if request.method == "POST":
            username = request.get("username")
            password = request.get("password")
            db.add_user(username, password)  # Save user to DB

            # Render success message in register page
            context = {"message": f"Welcome, {username}! Registration successful."}
            return Response(template_engine.render("register.html", context))

        # Render register form
        return Response(template_engine.render("register.html"))

# Create an instance of the AuthController
auth_controller = AuthController()
