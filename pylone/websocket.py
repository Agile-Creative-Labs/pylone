"""
    WebSocketServer Class

    A generic WebSocket server class that handles WebSocket connections and messaging.
    This class provides a simple way to integrate real-time communication into your Python framework.

    Features:
    - Manages WebSocket connections and automatically registers/unregisters clients.
    - Broadcasts incoming messages to all connected clients.
    - Customizable handler for processing messages.
    - Logs connection events and received messages.

    Usage Example:

    # Initialize the WebSocket server
    server = WebSocketServer(host='localhost', port=8765)

    # Start the WebSocket server
    server.start()

    Attributes:
        host (str): The host address to bind the WebSocket server.
        port (int): The port number to bind the WebSocket server.
        clients (set): A set of connected WebSocket clients.
    
    Author: Agile Creative Labs Inc
    Date: 2024-06-25 
    Version: 1.0        
"""
import asyncio
import websockets
import logging
from typing import Callable, Awaitable

class WebSocketServer:
    """
    A generic WebSocket server class that handles WebSocket connections and messaging.

    Attributes:
        host (str): The host address to bind the WebSocket server.
        port (int): The port number to bind the WebSocket server.
        handler (Callable[[websockets.WebSocketServerProtocol, str], Awaitable[None]]):
            A callback function to handle incoming messages.
    """

    def __init__(self, host: str = 'localhost', port: int = 8765):
        """
        Initialize the WebSocketServer.

        Args:
            host (str): The host address to bind the WebSocket server. Defaults to 'localhost'.
            port (int): The port number to bind the WebSocket server. Defaults to 8765.
        """
        self.host = host
        self.port = port
        self.clients = set()

    async def handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """
        Handle incoming WebSocket connections and messages.

        Args:
            websocket (websockets.WebSocketServerProtocol): The WebSocket connection.
            path (str): The path of the WebSocket connection.
        """
        # Register client
        self.clients.add(websocket)
        try:
            async for message in websocket:
                logging.info(f"Received message: {message}")
                # Broadcast the message to all connected clients
                await self.broadcast(message)
        except websockets.ConnectionClosed:
            logging.info("Connection closed")
        finally:
            # Unregister client
            self.clients.remove(websocket)

    async def broadcast(self, message: str):
        """
        Broadcast a message to all connected clients.

        Args:
            message (str): The message to broadcast.
        """
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    def start(self):
        """
        Start the WebSocket server.
        """
        start_server = websockets.serve(self.handler, self.host, self.port)
        logging.info(f"WebSocket server started at ws://{self.host}:{self.port}")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = WebSocketServer(host='localhost', port=8765)
    server.start()
