"""
Development Configuration Module for Demo Application.

This module defines the development configuration settings for the demo
application. It extends the base Config class from pylone.settings and
provides specific configurations for development environments, such as
enabling debug mode and setting the database name and URI.

Imports:
    os: For interacting with the operating system (e.g., environment variables).
    pylone.settings.Config: The base configuration class.

Classes:
    DevelopmentConfig: Configuration class for development environments.

Usage:
    - This module should be imported to access the development configuration settings.

Author: Agile Creative Labs Inc
Date: 2024-06-25 (Replace with today's date)
Version: 1.0
"""
import os
from pylone.settings import Config  # Import the base Config class

class DevelopmentConfig(Config):
    """Configuration for the demo app."""
    DEBUG = True
    DB_NAME = os.getenv('DB_NAME', 'demo.db')  # Default to 'demo.db' if not set
    DATABASE_URI = f"sqlite:///{DB_NAME}"  # Use DB_NAME to construct the DATABASE_URI
    ALLOWED_PATHS = [
            "/",
            "/login",
            "/register",
            "/demo",
            "/ajax-demo",
            "/ajax/data",
            "/test-json",
            "/test-response-object",
            "/test-raw-tuple",
            "/test-json-response",
            "/test-text-response",
            "/test-invalid-response",
            "/test-raw-bytes",
            "/test-links"
        ]

# Create an instance of the configuration
config = DevelopmentConfig()