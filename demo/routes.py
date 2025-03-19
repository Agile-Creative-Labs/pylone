"""
Routing Configuration for Demo Application.

This module defines the URL routing for the demo application using the
pylone.router.Router class. It maps URL paths to corresponding controller
methods, handling authentication, dashboard, AJAX, and test functionalities.

Imports:
    pylone.router.Router: The router class for handling URL routing.
    demo.controllers.auth_controller.auth_controller: The authentication controller instance.
    demo.controllers.dashboard_controller.dashboard_controller: The dashboard controller instance.
    demo.controllers.ajax_controller.ajax_controller: The AJAX controller instance.
    demo.controllers.test_controller.TestController: The test controller class.

Usage:
    - This module should be imported to initialize the URL routing for the application.

Author: Agile Creative Labs Inc
Date: 2024-06-25 (Replace with today's date)
Version: 1.0
"""

#demo/routes.py
from pylone.router import Router
from demo.controllers.auth_controller import auth_controller
from demo.controllers.dashboard_controller import dashboard_controller
from demo.controllers.ajax_controller import ajax_controller
from demo.controllers.test_controller import TestController

# Create a router
router = Router()

# Route paths
LOGIN_ROUTE = "/login"
REGISTER_ROUTE = "/register"
DASHBOARD_ROUTE = "/dashboard"
AJAX_DATA_ROUTE = "/ajax/data"
AJAX_DEMO_ROUTE = "/ajax-demo"

# Authentication routes
router.add_route("/", auth_controller.welcome, methods=["GET", "POST"])  # Default route to login page
router.add_route(LOGIN_ROUTE, auth_controller.login, methods=["GET", "POST"])  # Login page
router.add_route(REGISTER_ROUTE, auth_controller.register, methods=["GET", "POST"])  # User registration page
router.add_route("/logout", dashboard_controller.logout, methods=["GET"])  # Logout route

# Dashboard routes
router.add_route(DASHBOARD_ROUTE, dashboard_controller.dashboard, methods=["GET"])  # Dashboard page
router.add_route("/add_user", dashboard_controller.add_user_page, methods=["GET", "POST"])  # Add user page
router.add_route("/edit_user/<int:user_id>", dashboard_controller.edit_user_page, methods=["GET", "POST"])  # Edit user page
router.add_route("/delete_user/<int:user_id>", dashboard_controller.delete_user_page, methods=["GET"])  # Delete user page

# Demo and AJAX routes
router.add_route("/demo", auth_controller.demo, methods=["GET"])  # Demo page
router.add_route(AJAX_DATA_ROUTE, ajax_controller.get_data, methods=["GET"])  # AJAX data provider
router.add_route(AJAX_DEMO_ROUTE, ajax_controller.ajax_demo, methods=["GET"])  # AJAX demo page
router.add_route("/test-json", ajax_controller.test_json_response, methods=["GET"])

# Mock tests
test_controller = TestController()
router.add_route("/test-response-object", test_controller.test_response_object, methods=["GET"])
router.add_route("/test-raw-tuple", test_controller.test_raw_tuple, methods=["GET"])
router.add_route("/test-json", test_controller.test_json_response, methods=["GET"])
router.add_route("/test-text", test_controller.test_text_response, methods=["GET"])
router.add_route("/test-raw-bytes", test_controller.test_raw_bytes_response, methods=["GET"])
router.add_route("/test-invalid", test_controller.test_invalid_response, methods=["GET"])
router.add_route("/test-links",test_controller.links, methods=["GET"])

# Fallback route for 404 errors
#TODO: Implement this router.add_route("/404", error_controller.not_found, methods=["GET"])

# Error handler for exceptions
#def handle_error(request, exception):
#    return error_controller.internal_server_error(request)

#router.set_error_handler(handle_error)