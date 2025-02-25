from pylone.request import Request
from pylone.response import Response
from pylone.template import TemplateEngine
from pylone.session import SessionManager

template_engine = TemplateEngine("demo/templates")

class DashboardController:
    @staticmethod
    def dashboard(request: Request):
        session_id = request.query_params.get("session", [""])[0]
        user_id = SessionManager.get_user(session_id)
        
        if user_id:
            return Response(template_engine.render("dashboard.html", {"user_id": user_id}))
        return Response("Unauthorized", status=401)
