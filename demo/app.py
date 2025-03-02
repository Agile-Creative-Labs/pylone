"""
Application Setup Module for Demo Application.

This module initializes and configures the main WSGI application for the
demo application. It sets up logging, determines the static file directory,
creates the base application instance, and wraps it with necessary
middleware components.

Imports:
    demo.middlewares.staticfile_middleware.StaticFileMiddleware: Middleware for serving static files.
    demo.settings.config: Configuration settings for the application.
    logging: For logging messages.
    os: For interacting with the operating system (e.g., file paths).
    pylone.app.App: The main application class.
    pylone.router.router: The router instance for handling URL routing.
    demo.middlewares.logging_middleware.LoggingMiddleware: Middleware for logging requests and responses.
    demo.middlewares.auth_middleware.AuthMiddleware: Middleware for handling authentication.

Usage:
    - This module should be executed to initialize the application before running the WSGI server.

Author: Agile Creative Labs Inc
Date: 2024-06-25 
Version: 1.0
"""

import os
from whitenoise import WhiteNoise
from pylone.app import App
from demo.routes import router
from demo.middlewares.logging_middleware import LoggingMiddleware
from demo.middlewares.auth_middleware import AuthMiddleware
from demo.middlewares.staticfile_middleware import StaticFileMiddleware
from demo.settings import config  # Import the config object
import logging


# Determine the path to the static directory
static_dir = os.path.join(os.path.dirname(__file__), 'static')
logging.info(f"Static directory: {static_dir}")  # Add this line

# Create the base app
app = App(router)

# Setup the app (call setup before wrapping with middlewares)
app.setup(router)

# Wrap the app with middlewares
app = LoggingMiddleware(app)  
app = StaticFileMiddleware(app, static_dir=static_dir)  
app = AuthMiddleware(app)  
