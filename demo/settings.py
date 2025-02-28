import os
from pylone.settings import Config  # Import the base Config class

class DevelopmentConfig(Config):
    """Configuration for the demo app."""
    DEBUG = True
    DB_NAME = os.getenv('DB_NAME', 'demo.db')  # Default to 'demo.db' if not set
    DATABASE_URI = f"sqlite:///{DB_NAME}"  # Use DB_NAME to construct the DATABASE_URI

# Create an instance of the configuration
config = DevelopmentConfig()