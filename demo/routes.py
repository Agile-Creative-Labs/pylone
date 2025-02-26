from pylone.router import Router
from demo.controllers.auth_controller import login, register
from demo.controllers.dashboard_controller import dashboard

router = Router()

# Define routes and map them to controllers
router.add_route("/", login)  # Default route to login page
router.add_route("/login", login)
router.add_route("/register", register)
router.add_route("/dashboard", dashboard)
print("Registered Routes:")
for path, route in router.routes.items():
    print(f"Path: {path} -> Handler: {route['handler'].__name__}")
