import logging
from pylone.response import Response
from pylone.session import session_manager
from demo.database import create_connection, add_user, get_user

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def login(request):
    """Handles the login page."""
    if request.method == "POST":
        username = request.get("username")
        password = request.get("password")
        conn = create_connection()
        user = get_user(conn, username)
        conn.close()

        if user and user[2] == password:  # Check if password matches
            # Create a session for the user
            session_id = session_manager.create_session(user[0])  # user[0] is the user ID
            # Redirect to the dashboard with a session cookie
            return Response("", status=302, headers=[("Location", "/dashboard")], cookies={"session_id": session_id})
        else:
            return Response("<h1>Login Failed</h1><p>Invalid username or password.</p>", status=401)

    # Display the login form
    return Response("""
        <h1>Login</h1>
        <form method="POST" action="/login">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br>
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <a href="/register">Register here</a>.</p>
    """)

def register(request):
    """Handles the registration page."""
    if request.method == "POST":
        username = request.get("username")
        password = request.get("password")
        if not username or not password:
            return Response("<h1>Registration Failed</h1><p>Username and password are required.</p>", status=400)

        conn = create_connection()
        add_user(conn, username, password)
        conn.close()
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