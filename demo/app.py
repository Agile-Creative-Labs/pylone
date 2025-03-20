"""
Filename: app.py

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
from demo.routes import router
from demo.middlewares.logging_middleware import LoggingMiddleware
from demo.middlewares.auth_middleware import AuthMiddleware
from demo.middlewares.staticfile_middleware import StaticFileMiddleware
from demo.settings import config

from wsgiref.simple_server import make_server


# Determine the path to the static directory
static_dir = os.path.join(os.path.dirname(__file__), 'static')
logging.info(f"Static directory: {static_dir}")

# Create the base app
base_app = App(router)

# Setup the app (call setup before wrapping with middlewares)
base_app.setup(router)

# Example WebSocket route
async def chat_handler(websocket):
    await websocket.send("Welcome to the chat!")
    async for message in websocket:
        await websocket.send(f"Echo: {message}")

# Add WebSocket route
base_app.add_websocket_route("/chat", chat_handler)

# Wrap the app with middlewares for WSGI processing
wsgi_app = LoggingMiddleware(base_app)
wsgi_app = StaticFileMiddleware(wsgi_app, static_dir=static_dir)
wsgi_app = AuthMiddleware(wsgi_app)

# Create a proxy app that maintains the run method while using the middleware stack for WSGI calls
import asyncio
import threading

class AppProxy:
    def __init__(self, base_app: App, wsgi_app: Callable):
        self.base_app = base_app
        self.wsgi_app = wsgi_app
        self.websocket_thread = None
        self.http_thread = None
        self.loop = None
        self.http_server = None
        self.shutdown_event = threading.Event()  # Used for clean shutdown

    def __call__(self, environ: Dict[str, Any], start_response: Callable) -> Any:
        return self.wsgi_app(environ, start_response)

    def run(self, http_host: str = "127.0.0.1", http_port: int = 8000, ws_host: str = "127.0.0.1", ws_port: int = 8001) -> None:
        """Start HTTP and WebSocket servers."""
        
        # Start the WebSocket server in a separate thread
        if hasattr(self.base_app, "websocket_wrapper"):
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.websocket_thread = threading.Thread(
                target=self._run_websocket_server,
                args=(ws_host, ws_port),
                daemon=True
            )
            self.websocket_thread.start()

        # Start HTTP server in a separate thread
        self.http_server = make_server(http_host, http_port, self)
        self.http_thread = threading.Thread(target=self._run_http_server, daemon=True)
        self.http_thread.start()

        logging.info(f"🚀 HTTP server running on http://{http_host}:{http_port}")

        # Wait for shutdown signal
        self.shutdown_event.wait()
        self.shutdown()

    def _run_http_server(self):
        """Helper function to run the HTTP server."""
        try:
            self.http_server.serve_forever()
        except Exception as e:
            logging.error(f"HTTP server encountered an error: {e}")

    def x_run_websocket_server(self, ws_host, ws_port):
        """Runs the WebSocket server in a separate thread."""
        try:
            self.loop.run_until_complete(self.base_app.start_websocket_server(ws_host, ws_port))
        except asyncio.CancelledError:
            logging.info("WebSocket server task was cancelled.")
        except Exception as e:
            logging.error(f"Unexpected error in WebSocket server: {e}")
        finally:
            logging.info("WebSocket server thread exiting...")


    async def _stop_event_loop(self):
        """Stop the event loop safely by ensuring all tasks are canceled."""
        tasks = [task for task in asyncio.all_tasks() if not task.done()]
        for task in tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        self.loop.stop()

    def x_________shutdown(self):
        """Shutdown the HTTP server, WebSocket server, and event loop cleanly."""
        logging.info("Shutting down servers gracefully...")

        # Shutdown HTTP server
        if self.http_server:
            logging.info("Shutting down HTTP server...")
            self.http_server.shutdown()
            self.http_thread.join()
            logging.info("HTTP server shut down.")

        # Shutdown WebSocket server properly
        if self.websocket_thread and self.websocket_thread.is_alive():
            logging.info("Shutting down WebSocket server...")

            if self.loop and self.loop.is_running():
                # Stop the WebSocket server safely
                future = asyncio.run_coroutine_threadsafe(self._shutdown_websockets(), self.loop)
                future.result()  # Ensure completion before proceeding

            self.websocket_thread.join()
            logging.info("WebSocket server shut down.")

        self.shutdown_event.set()  # Signal the run() method to exit
        logging.info("All servers shut down gracefully. Exiting...")

    async def _shutdown_websockets(self):
        """Stop the WebSocket server and clean up all tasks properly."""
        logging.info("Cancelling pending WebSocket tasks...")
        tasks = [task for task in asyncio.all_tasks(self.loop) if not task.done()]
        for task in tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        self.loop.stop()  # Stop the event loop

    def _run_websocket_server(self, ws_host, ws_port):
        """Runs the WebSocket server in a separate thread."""
        try:
            self.loop.run_until_complete(self.base_app.start_websocket_server(ws_host, ws_port))
        except asyncio.CancelledError:
            logging.info("WebSocket server task was cancelled.")
        except Exception as e:
            logging.error(f"Unexpected error in WebSocket server: {e}")
        finally:
            self.loop.stop()  # <- Stop the event loop to allow full shutdown
            logging.info("WebSocket server thread exiting...")
    
    def shutdown(self):
        """Shuts down the application, including HTTP and WebSocket servers."""
        logging.info("Shutting down servers gracefully...")

        # Shutdown HTTP server
        if hasattr(self, "http_server") and self.http_server:
            logging.info("Shutting down HTTP server...")
            self.http_server.shutdown()
            logging.info("HTTP server shut down.")
    
        # Gracefully handle WebSocket server shutdown
        if hasattr(self, "ws_server"):
            if self.ws_server:
                logging.info("Shutting down WebSocket server...")
                try:
                    for task in asyncio.all_tasks(self.loop):
                        task.cancel()
                        self.loop.stop()
                        logging.info("WebSocket server shut down.")
                except Exception as e:
                    logging.error(f"Error shutting down WebSocket server: {e}")
            else:
                logging.info("WebSocket server was already None. No action needed.")
        else:
            logging.info("WebSocket server was never initialized. Skipping shutdown.")

        logging.info("All servers shut down gracefully. Exiting...")

# Create the proxy app
app = AppProxy(base_app, wsgi_app)
