from pylone.router import Router
from demo.controllers.auth_controller import auth_controller
from demo.controllers.dashboard_controller import dashboard_controller

# Create a router
router = Router()

# Define routes and map them to controllers
router.add_route("/", auth_controller.login, methods=["GET", "POST"])  # Default route to login page
router.add_route("/login", auth_controller.login, methods=["GET", "POST"])
router.add_route("/register", auth_controller.register, methods=["GET", "POST"])
router.add_route("/dashboard", dashboard_controller.dashboard, methods=["GET"])
router.add_route("/add_user", dashboard_controller.add_user_page, methods=["GET", "POST"])
router.add_route("/edit_user/<int:user_id>", dashboard_controller.edit_user_page, methods=["GET", "POST"])
router.add_route("/delete_user/<int:user_id>", dashboard_controller.delete_user_page, methods=["GET"])
router.add_route("/logout", dashboard_controller.logout, methods=["GET"])  # Logout route