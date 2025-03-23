"""
Filename: demo/app.py

Description:
This script sets up a web application using the `pylone.app.App` framework. It includes:
- Route management using the provided `router`.
- Middlewares for logging, authentication, and serving static files.
- A WebSocket route for chat functionality.
- A proxy class (`AppProxy`) to manage HTTP and WebSocket servers concurrently.

Key Features:
- Graceful shutdown of both HTTP and WebSocket servers.
- Logging for server activities and error handling.
- Static file serving from a predefined directory.

Dependencies:
- pylone
- whitenoise
- demo (custom application modules)

Usage:
Run this script to start both HTTP and WebSocket servers. HTTP server listens on port 8000 by default, and WebSocket server listens on port 8001.

Author: Agile Creative Labs Inc
Date: 2024-06-25 
Version: 1.0
"""
# demo/app.py
import os
import logging
import signal
import threading
import sys
import asyncio

from whitenoise import WhiteNoise
from typing import Callable, Dict, Any  # Add this import
from pylone.app import App
from pylone.app_proxy import AppProxy
from demo.routes import router
from demo.middlewares.logging_middleware import LoggingMiddleware
from demo.middlewares.auth_middleware import AuthMiddleware
from demo.middlewares.staticfile_middleware import StaticFileMiddleware
from demo.settings import config

from wsgiref.simple_server import make_server
#nlp test
from pylone.chat_handler import ChatHandler  # Import the ChatHandler
import spacy  # Import SpaCy for NLP


# Determine the path to the static directory
static_dir = os.path.join(os.path.dirname(__file__), 'static')
logging.info(f"Static directory: {static_dir}")

# Create the base app
base_app = App(router)

# Setup the app (call setup before wrapping with middlewares)
base_app.setup(router)

# WebSocket route
'''
async def chat_handler(websocket):
    await websocket.send(config.CHAT_GREETING)
    async for message in websocket:
        await websocket.send(f"Echo: {message}")

# Add WebSocket route
base_app.add_websocket_route("/chat", chat_handler)
'''

# Load a SpaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize the ChatHandler with a greeting and the NLP model
chat_handler_instance = ChatHandler(greeting=config.CHAT_GREETING, nlp_model=nlp)

# Define a WebSocket route using the ChatHandler instance
async def chat_route(websocket):
    await chat_handler_instance.handle_chat(websocket)

# Add the WebSocket route to the base app
base_app.add_websocket_route("/chat", chat_route)

# Wrap the app with middlewares for WSGI processing
wsgi_app = LoggingMiddleware(base_app)
wsgi_app = StaticFileMiddleware(wsgi_app, static_dir=static_dir)
wsgi_app = AuthMiddleware(wsgi_app)

# Create the proxy app
app = AppProxy(base_app, wsgi_app)
