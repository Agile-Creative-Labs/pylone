from pylone.response import Response
from pylone.template import TemplateEngine
import os

# Initialize template engine with the correct template directory
template_engine = TemplateEngine(os.path.join(os.path.dirname(__file__), "../templates"))

def login(request):
    """Handles the login page."""
    return Response(template_engine.render("login.html"))

def register(request):
    """Handles the register page."""
    return Response(template_engine.render("register.html"))
