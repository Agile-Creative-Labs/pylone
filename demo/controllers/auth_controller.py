#demo/controllers/auth_controller.py
from pylone.response import Response
from pylone.template import TemplateEngine
import os
import logging

# Initialize template engine with the correct template directory
template_engine = TemplateEngine(os.path.join(os.path.dirname(__file__), "../templates"))

def login(request):
    """Handles the login page."""
    logging.debug("Login handler called")
    return Response(template_engine.render("login.html"))

def register(request):
    """Handles the register page."""
    return Response(template_engine.render("register.html"))
