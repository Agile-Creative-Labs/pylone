from pylone.response import Response
from pylone.template import TemplateEngine
import os

template_engine = TemplateEngine(os.path.join(os.path.dirname(__file__), "../templates"))

def dashboard(request):
    """Handles the dashboard page."""
    return Response(template_engine.render("dashboard.html"))
