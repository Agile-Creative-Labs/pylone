from demo.controllers.auth_controller import AuthController
from demo.controllers.dashboard_controller import DashboardController

def setup_routes(app):
    app.add_route("/", AuthController.index)
    app.add_route("/register", AuthController.register, methods=["GET", "POST"])
    app.add_route("/login", AuthController.login, methods=["GET", "POST"])
    app.add_route("/dashboard", DashboardController.dashboard)
