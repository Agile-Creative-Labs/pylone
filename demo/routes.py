from pylone.router import Router
from demo.controllers.auth_controller import login, register
from demo.controllers.dashboard_controller import dashboard

# Create a router
router = Router()

# Define routes and map them to controllers
router.add_route("/", login, methods=["GET"])  # Default route to login page
router.add_route("/login", login, methods=["GET"])
router.add_route("/register", register, methods=["GET"])
router.add_route("/dashboard", dashboard, methods=["GET"])
