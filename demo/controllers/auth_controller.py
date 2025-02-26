from demo.database import db  # Import the database instance
from pylone.response import Response
from pylone.session import session_manager
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class AuthController:
    def login(self, request):
        """Handles the login page."""
        if request.method == "POST":
            username = request.get("username")
            password = request.get("password")
            user = db.get_user(username)  # Use the database instance

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
                return Response("<h1>Login Failed</h1><p>Invalid username or password.</p>", status=401)

        # Display the login form
        return Response("""
            <h1>Login</h1>
            <form method="POST">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required><br>
                <button type="submit">Login</button>
            </form>
            <p>Don't have an account? <a href="/register">Register here</a>.</p>
        """)

    def register(self, request):
        """Handles the registration page."""
        if request.method == "POST":
            username = request.get("username")
            password = request.get("password")
            db.add_user(username, password)  # Use the database instance
            return Response(f"<h1>Registration Successful!</h1><p>Welcome, {username}!</p>")

        # Display the registration form
        return Response("""
            <h1>Register</h1>
            <form method="POST">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required><br>
                <button type="submit">Register</button>
            </form>
            <p>Already have an account? <a href="/login">Login here</a>.</p>
        """)

# Create an instance of the AuthController
auth_controller = AuthController()