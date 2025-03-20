# pylone/websocket.py
import asyncio
import logging
import re
from websockets import serve

class WebSocketWrapper:
    """Wrapper for handling WebSocket connections."""
    
    def __init__(self):
        self.websocket_routes = {}
        self.clients = set()
        
    def add_route(self, path, handler):
        """
        Register a WebSocket route.
        
        Args:
            path (str): The URL path for the WebSocket route.
            handler (callable): The coroutine function to handle WebSocket connections.
        """
        # Convert dynamic route parameters to a regex pattern
        pattern = re.sub(r"<(\w+:)?(\w+)>", r"(?P<\2>[^/]+)", path)
        self.websocket_routes[path] = {
            "pattern": re.compile(f"^{pattern}$"),
            "handler": handler
        }
        logging.info(f"WebSocket Route Added: {path}")
        
    async def handle_connection(self, websocket, path):
        """
        Handle an incoming WebSocket connection.
        
        Args:
            websocket: The WebSocket connection object.
            path (str): The request path.
        """
        # Add client to the connected clients set
        self.clients.add(websocket)
        matched = False
        
        try:
            logging.info(f"New WebSocket connection: {path}")
            
            # Match the path to a registered WebSocket route
            for route_path, route_info in self.websocket_routes.items():
                match = route_info["pattern"].match(path)
                if match:
                    matched = True
                    handler = route_info["handler"]
                    kwargs = match.groupdict()
                    
                    # Call the handler with the websocket and any path parameters
                    if kwargs:
                        await handler(websocket, **kwargs)
                    else:
                        await handler(websocket)
                    break
            
            if not matched:
                logging.warning(f"No WebSocket handler found for path: {path}")
                await websocket.close(1003, "Path not found")
                
        except Exception as e:
            logging.error(f"Error in WebSocket handler: {e}")
        finally:
            # Remove client from the connected clients set
            if websocket in self.clients:
                self.clients.remove(websocket)
            
    async def broadcast(self, message, exclude=None):
        """
        Broadcast a message to all connected clients.
        
        Args:
            message (str): Message to broadcast.
            exclude: Optional client to exclude from broadcast.
        """
        for client in self.clients:
            if client != exclude and not client.closed:
                try:
                    await client.send(message)
                except Exception as e:
                    logging.error(f"Error broadcasting to client: {e}")
                    
    async def start(self, host="127.0.0.1", port=8001):
        """
        Start the WebSocket server.
        
        Args:
            host (str): Host address to bind to.
            port (int): Port to listen on.
        """
        async with serve(self.handle_connection, host, port):
            logging.info(f"WebSocket server started on ws://{host}:{port}")
            # Keep the server running
            await asyncio.Future()  # Run forever