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
import json
import traceback

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
        return Response(
            self.template_engine.render(
                "public/demo.html", {"title": "Demo Page", "crew": mock_data}
            )
        )

    def welcome(self, request):
        return Response(
            self.template_engine.render("public/welcome.html", {"error": ""})
        )

    def xregister(self, request):
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
                    return Response(
                        self.template_engine.render(
                            "public/register.html",
                            {
                                "message": f"Welcome, {username}! Registration successful."
                            },
                        ),
                        status=200,
                    )
                else:
                    logging.error(
                        "Failed to register user (possible duplicate username)"
                    )
                    return Response(
                        self.template_engine.render(
                            "public/register.html",
                            {
                                "error": "Username already exists or an error occurred during registration."
                            },
                        ),
                        status=400,
                    )

            except Exception as e:
                logging.error(f"Exception during registration: {e}")
                return Response(
                    self.template_engine.render(
                        "public/register.html",
                        {"error": "An unexpected error occurred. Please try again."},
                    ),
                    status=500,
                )

            # Render the register form for GET request
        logging.debug("Rendering register form")
        return Response(
            self.template_engine.render("public/register.html", {}), status=200
        )

    def logout(self, request):
        """Handles user logout."""
        logging.debug("Handling logout request")
        session_id = request.cookies.get("session_id")

        if session_id:
            session_manager.destroy_session(session_id)

        return Response(
            "", status=302, headers={"Location": "/login"}, cookies={"session_id": ""}
        )

    def auth(self, request):
        """Handles the login page."""
        if request.method == "POST":
            username = request.get("username")
            password = request.get("password")
            user = db.get_user(username)  # Fetch user from DB

            if user and user[2] == password:  # Check if password matches
                # Create a session for the user
                session_id = session_manager.create_session(
                    user[0]
                )  # user[0] is the user ID

                # Respond with JSON including the redirect URL
                return Response(
                    {"message": "Login successful!", "redirect": "/dashboard"},
                    status=200,
                    headers={"Content-Type": "application/json"},
                    cookies={"session_id": session_id},
                )
            else:
                # Return JSON error response
                return Response(
                    {"error": "Invalid username or password."},
                    status=401,
                    headers={"Content-Type": "application/json"},
                )

        # Return an error for unsupported methods
        return Response(
            {"error": "Unsupported request method."},
            status=405,
            headers={"Content-Type": "application/json"},
        )

    def _json_response(self, data, status=200):
        response = {
            "status": status,
            "data": data,
        }
        return json.dumps(response), status, {"Content-Type": "application/json"}

    def json_response(self, data, status=200):
        return Response(
            body=data, status=status, headers={"Content-Type": "application/json"}
        )

    def verify_password(self, input_password, stored_password):
        # Implement password hashing and verification logic here
        return (
            input_password == stored_password
        )  # Placeholder: Replace with actual verification

    def login(self, request):
        """Handles the login page and login requests."""
        if request.method == "POST":
            try:
                # Get and validate request data
                request_data = request.body

                if not isinstance(request_data, dict) or not request_data:
                    logging.warning("Invalid or empty request body for login")
                    return self.json_response(
                        {"error": "Invalid request format"}, status=400
                    )

                username = request_data.get("username")
                password = request_data.get("password")

                # Validate required fields
                if not username or not password:
                    logging.warning(
                        f"Missing credentials: username={bool(username)}, password={bool(password)}"
                    )
                    return self.json_response(
                        {"error": "Username and password are required"}, status=400
                    )

                # Get user and validate credentials
                user = db.get_user(username)
                logging.debug(f"User lookup result: {user is not None}")

                if not user:
                    logging.warning(
                        f"Login attempt with non-existent username: {username}"
                    )
                    # Use generic error message for security
                    return self.json_response(
                        {"error": "Invalid credentials"}, status=401
                    )

                if len(user) < 3:
                    logging.error(f"Invalid user data structure for {username}")
                    return self.json_response({"error": "System error"}, status=500)

                if not self.verify_password(password, user[2]):
                    logging.warning(f"Failed login attempt for user: {username}")
                    # Use generic error message for security
                    return self.json_response(
                        {"error": "Invalid credentials"}, status=401
                    )

                # Authentication successful
                logging.info(f"Successful login for user: {username}")

                # Create session
                session_id = session_manager.create_session(user[0])

                # Set session cookie and return success with redirect
                response = Response(
                    body={
                        "success": True,
                        "message": "Login successful",
                        "redirect": "/dashboard",
                    },
                    status=200,
                    headers={"Content-Type": "application/json"},
                )

                # Set secure session cookie
                response.set_cookie(
                    "session_id",
                    session_id,
                    httponly=True,  # Prevent JavaScript access
                    secure=True,  # HTTPS only
                    samesite="Lax",  # CSRF protection
                    path="/",  # Available throughout site
                    max_age=86400,
                )  # 24 hours

                return response

            except Exception as e:
                logging.error(f"Login error: {e}", exc_info=True)
                return self.json_response(
                    {"error": "An unexpected error occurred"}, status=500
                )

        elif request.method == "GET":
            return Response(
                self.template_engine.render("public/login.html", {"error": ""}),
                headers={"Content-Type": "text/html"},
            )

        return self.json_response({"error": "Method not allowed"}, status=405)

    def register(self, request):
        """Handles the registration process."""
        logging.debug("Handling register request")

        if request.method == "POST":
            logging.debug("Processing POST request for registration")

            try:
                # Get email and password directly from request.body which is already a dict
                email = request.body.get("email")
                password = request.body.get("password")

                # Attempt to save the new user to the database
                result = db.add_user(email, password)
                logging.debug(f"db.add_user returned: {result}")

                if result:
                    logging.info(f"New user successfully registered: {email}")
                    # Assuming your Response class doesn't take content_type parameter
                    return Response(
                        json.dumps(
                            {"message": f"Welcome, {email}! Registration successful."}
                        ),
                        status=200,
                    )
                else:
                    logging.warning("Registration failed - possible duplicate email")
                    return Response(
                        json.dumps(
                            {
                                "error": "This email is already registered. Please use another or log in."
                            }
                        ),
                        status=400,
                    )

            except Exception as e:
                logging.error(f"An exception occurred during registration: {e}")
                return Response(
                    json.dumps(
                        {
                        "error": "An unexpected server error occurred. Please try again later."
                        }
                    ),
                    status=500,
                )

        # Handle GET requests (render registration form)
        logging.debug("Rendering registration form")
        return Response(self.template_engine.render("public/register.html", {}), status=200)


# Create an instance of the AuthController with the template engine
auth_controller = AuthController(template_engine)
