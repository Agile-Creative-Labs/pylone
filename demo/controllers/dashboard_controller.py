#template_engine = TemplateEngine(os.path.join(os.path.dirname(__file__), "../templates"))
#def dashboard(request):
#    """Handles the dashboard page."""
#    return Response(template_engine.render("dashboard.html"))

import logging
from pylone.response import Response
from pylone.session import session_manager
from pylone.template import TemplateEngine   # Ensure this imports Jinja2 template engine
import logging
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize TemplateEngine with the templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../templates/")
template_engine = TemplateEngine(TEMPLATES_DIR)

class DashboardController:
    def __init__(self, template_engine):
        self.template_engine = template_engine

    def dashboard(self, request):
        """Handles the dashboard page."""
        logging.debug("Handling dashboard request")

        # Get user session
        session_id = request.cookies.get("session_id")
        user_id = session_manager.get_session(session_id)

        if not user_id:
            logging.debug("No active session, redirecting to login.")
            return Response("", status=302, headers={"Location": "/login"})

        # Mock user details (In real case, fetch from DB)
        user_data = {"id": user_id, "username": "JohnDoe"}

        return Response(self.template_engine.render("private/dashboard.html", {
            "title": "Dashboard",
            "user": user_data
        }), status=200)




    def add_user_page(self, request):
        """Handles the add user page."""
        if request.method == "POST":
            username = request.get("username")
            password = request.get("password")
            db.add_user(username, password)  # Use the database instance
            return Response("", status=302, headers=[("Location", "/dashboard")])

        # Display the add user form
        return Response("""
            <h1>Add New User</h1>
            <form method="POST">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required><br>
                <button type="submit">Add User</button>
            </form>
            <br>
            <a href="/dashboard">Back to Dashboard</a>
        """)
    def edit_user_page(self, request, user_id):
        """Handles the edit user page."""
        user = db.get_user_by_id(user_id)  # Use the database instance

        if not user:
            return Response("<h1>User Not Found</h1>", status=404)

        if request.method == "POST":
            username = request.get("username")
            password = request.get("password")
            db.update_user(user_id, username, password)  # Use the database instance
            return Response("", status=302, headers=[("Location", "/dashboard")])

        # Render the edit user form
        context = {
            'user_id': user_id,
            'username': user[1],
            'password': user[2],
            'dashboard_url': '/dashboard'
        }
        edit_user_html = self.template_engine.render('edit_user.html', context)
        return Response(edit_user_html, status=200)
    
    def ___edit_user_page(self, request, user_id):
        """Handles the edit user page."""
        user = db.get_user_by_id(user_id)  # Use the database instance

        if not user:
            return Response("<h1>User Not Found</h1>", status=404)

        if request.method == "POST":
            username = request.get("username")
            password = request.get("password")
            db.update_user(user_id, username, password)  # Use the database instance
            return Response("", status=302, headers=[("Location", "/dashboard")])

        # Display the edit user form
        return Response(f"""
            <h1>Edit User</h1>
            <form method="POST">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" value="{user[1]}" required><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" value="{user[2]}" required><br>
                <button type="submit">Update User</button>
            </form>
            <br>
            <a href="/dashboard">Back to Dashboard</a>
        """)

    def delete_user_page(self, request, user_id):
        """Handles the delete user action."""
        db.delete_user(user_id)  # Use the database instance
        return Response("", status=302, headers=[("Location", "/dashboard")])

    def logout(self, request):
        """Handles the logout action."""
        session_id = request.cookies.get("session_id")
        if session_id:
            session_manager.delete_session(session_id)  # Delete the session
        return Response("", status=302, headers=[("Location", "/login")])  # Redirect to login page


# Create an instance of DashboardController
dashboard_controller = DashboardController(template_engine)