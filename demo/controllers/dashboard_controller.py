from pylone.response import Response
from pylone.template import TemplateEngine
from pylone.session import session_manager
import os


#template_engine = TemplateEngine(os.path.join(os.path.dirname(__file__), "../templates"))
#def dashboard(request):
#    """Handles the dashboard page."""
#    return Response(template_engine.render("dashboard.html"))

def dashboard(request):
    """Handles the dashboard page."""
    session_id = request.cookies.get("session_id")
    session = session_manager.get_session(session_id)

    if session:
        user_id = session["user_id"]
        return Response(f"<h1>Dashboard</h1><p>Welcome to your dashboard, User #{user_id}!</p>")
    else:
        # Redirect to login if no valid session
        return Response("", status=302, headers=[("Location", "/login")])

def logout(request):
    session_id = request.cookies.get("session_id")
    if session_id:
        session_manager.delete_session(session_id)
    return Response("", status=302, headers=[("Location", "/login")])