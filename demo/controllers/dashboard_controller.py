#template_engine = TemplateEngine(os.path.join(os.path.dirname(__file__), "../templates"))
#def dashboard(request):
#    """Handles the dashboard page."""
#    return Response(template_engine.render("dashboard.html"))

from demo.database import db  # Import the database instance
from pylone.response import Response
from pylone.session import session_manager

def dashboard(request):
    """Handles the dashboard page."""
    session_id = request.cookies.get("session_id")
    session = session_manager.get_session(session_id)

    if not session:
        # Redirect to login if no valid session
        return Response("", status=302, headers=[("Location", "/login")])

    users = db.get_all_users()  # Use the database instance

    # Render the dashboard with the list of users
    user_list = "".join(
        f"""
        <tr>
            <td>{user[1]}</td>
            <td>{user[2]}</td>
            <td>
                <a href="/edit_user/{user[0]}">Edit</a> |
                <a href="/delete_user/{user[0]}">Delete</a>
            </td>
        </tr>
        """ for user in users
    )

    return Response(f"""
        <h1>Dashboard</h1>
        <p>Welcome to your dashboard!</p>
        <h2>User List</h2>
        <table border="1">
            <tr>
                <th>Username</th>
                <th>Password</th>
                <th>Actions</th>
            </tr>
            {user_list}
        </table>
        <br>
        <a href="/add_user">Add New User</a>
    """)

def add_user_page(request):
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

def edit_user_page(request, user_id):
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

def delete_user_page(request, user_id):
    """Handles the delete user action."""
    db.delete_user(user_id)  # Use the database instance
    return Response("", status=302, headers=[("Location", "/dashboard")])