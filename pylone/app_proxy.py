# Create a proxy app that maintains the run method while using the middleware stack for WSGI calls
import asyncio
import threading
from pylone.app import App
from typing import Callable, Dict, Any  # Add this import
from wsgiref.simple_server import make_server
import logging

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