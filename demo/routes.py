from pylone.router import Router
from demo.controllers.auth_controller import login, register
from demo.controllers.dashboard_controller import dashboard, add_user_page, edit_user_page, delete_user_page, logout

# Create a router
router = Router()

# Define routes and map them to controllers
router.add_route("/", login, methods=["GET", "POST"])  # Default route to login page
router.add_route("/login", login, methods=["GET", "POST"])
router.add_route("/register", register, methods=["GET", "POST"])
router.add_route("/dashboard", dashboard, methods=["GET"])
router.add_route("/add_user", add_user_page, methods=["GET", "POST"])
router.add_route("/edit_user/<int:user_id>", edit_user_page, methods=["GET", "POST"])
router.add_route("/delete_user/<int:user_id>", delete_user_page, methods=["GET"])
router.add_route("/logout", logout, methods=["GET"])  # Logout route