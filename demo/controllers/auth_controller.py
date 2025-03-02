"""
Authentication Controller for Pylone Web Framework.

This module provides the AuthController class, which handles user authentication
and authorization functionalities, including login, logout, registration, and
a demo page with mock data.

Imports:
    demo.database.db: The database instance for user management.
    pylone.response.Response: The response object for creating HTTP responses.
    pylone.session.session_manager: The session manager for handling user sessions.
    pylone.template.TemplateEngine: The template engine for rendering HTML templates.
    logging: For logging messages.
    os: For interacting with the operating system (e.g., file paths).

Classes:
    AuthController: Handles user authentication and authorization.

Functions:
    None.

 Author: Agile Creative Labs Inc.
 Version: 1.0.0
 Date: 02/22/2024
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
    def __init__(self, template_engine):
        self.template_engine = template_engine
    
    def demo(self, request):
        """Simulates rendering mock data into a list view."""
        logging.debug("Handling demo page request")

        # Mock data: A list of dictionaries
        mock_data = [
            {"id": 1, "name": "Jean-Luc Picard", "role": "Captain"},
            {"id": 2, "name": "William Riker", "role": "First Officer"},
            {"id": 3, "name": "Data", "role": "Android"},
            {"id": 4, "name": "Geordi La Forge", "role": "Chief Engineer"},
            {"id": 5, "name": "Beverly Crusher", "role": "Chief Medical Officer"},
        ]

        # Render the demo.html template with the mock data
        return Response(self.template_engine.render("public/demo.html", {"title": "Demo Page", "crew": mock_data}))

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
                return Response(self.template_engine.render("public/login.html", {"error": "Invalid username or password."}))
        
        # Render login form
        return Response(self.template_engine.render("public/login.html", {"error": ""}))
    
    def register(self, request):
        """Handles the registration page."""
        logging.debug("Handling register request")

        if request.method == "POST":
            logging.debug("Processing POST request for registration")
            username = request.get("username")
            password = request.get("password")

            try:
                # Save user to DB
                result = db.add_user(username, password)
                logging.debug(f"db.add_user returned: {result}")

                if result:  # Ensure db.add_user() explicitly returns True on success
                    logging.info(f"New user registered: {username}")
                    return Response(self.template_engine.render("public/register.html", {"message": f"Welcome, {username}! Registration successful."}), status=200)
                else:
                    logging.error("Failed to register user (possible duplicate username)")
                    return Response(self.template_engine.render("public/register.html", {"error": "Username already exists or an error occurred during registration."}), status=400)

            except Exception as e:
                logging.error(f"Exception during registration: {e}")
                return Response(self.template_engine.render("public/register.html", {"error": "An unexpected error occurred. Please try again."}), status=500)

            # Render the register form for GET request
        logging.debug("Rendering register form")
        return Response(self.template_engine.render("public/register.html", {}), status=200)

    def logout(self, request):
        """Handles user logout."""
        logging.debug("Handling logout request")
        session_id = request.cookies.get("session_id")

        if session_id:
            session_manager.destroy_session(session_id)

        return Response("", status=302, headers={"Location": "/login"}, cookies={"session_id": ""})

# Create an instance of the AuthController with the template engine
auth_controller = AuthController(template_engine)
