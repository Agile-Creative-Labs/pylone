from pylone.request import Request
from pylone.response import Response
from pylone.template import TemplateEngine
from pylone.session import SessionManager
from demo.database import register_user, get_user
import bcrypt

template_engine = TemplateEngine("demo/templates")

class AuthController:
    @staticmethod
    def index(request: Request):
        return Response(template_engine.render("index.html"))

    @staticmethod
    def register(request: Request):
        if request.method == "POST":
            username = request.query_params.get("username", [""])[0]
            password = request.query_params.get("password", [""])[0]
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

            if register_user(username, hashed_password):
                return Response("Registration successful", status=200)
            return Response("Username already taken", status=400)

        return Response(template_engine.render("register.html"))

    @staticmethod
    def login(request: Request):
        if request.method == "POST":
            username = request.query_params.get("username", [""])[0]
            password = request.query_params.get("password", [""])[0]
            user = get_user(username)

            if user and bcrypt.checkpw(password.encode(), user[2].encode()):
                session_id = SessionManager.create_session(user[0])
                return Response(session_id, status=200)
            return Response("Invalid credentials", status=401)

        return Response(template_engine.render("login.html"))
