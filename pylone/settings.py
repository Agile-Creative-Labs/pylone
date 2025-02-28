import os

class Config:
    """Default configuration for the Pylone framework."""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    STATIC_FOLDER = 'static'
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///:memory:')