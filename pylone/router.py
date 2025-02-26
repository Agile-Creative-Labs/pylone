import re
import logging
from pylone.response import Response

logging.basicConfig(level=logging.DEBUG)

class Router:
    def __init__(self):
        """Initialize the router with an empty routes dictionary."""
        self.routes = {}

    def add_route(self, path, handler, methods=["GET"]):
        """
        Register a route with a handler.

        Args:
            path (str): The URL path for the route.
            handler (function): The function to handle the request.
            methods (list): List of HTTP methods allowed for the route (e.g., ["GET", "POST"]).
        """
        # Convert dynamic route parameters to a regex pattern
        pattern = re.sub(r"<(\w+:)?(\w+)>", r"(?P<\2>[^/]+)", path)
        self.routes[path] = {"pattern": re.compile(f"^{pattern}$"), "handler": handler, "methods": methods}
        logging.debug(f"Route added: {path} with methods {methods}")

    def resolve(self, request):
        """
        Resolve a request to the appropriate handler.

        Args:
            request (Request): The request object containing path and method.

        Returns:
            Response: A response object to send back to the client.
        """
        path = request.path
        method = request.method
        logging.debug(f"Resolving request: {method} {path}")

        # Check if the path matches any route
        for route_path, route in self.routes.items():
            match = route["pattern"].match(path)
            if match:
                logging.debug(f"Route found: {route_path}")
                # Check if the request method is allowed for the route
                if method in route["methods"]:
                    logging.debug(f"Method {method} allowed for {route_path}")
                    handler = route["handler"]
                    # Pass dynamic parameters to the handler
                    kwargs = match.groupdict()
                    response = handler(request, **kwargs)  # Call the handler
                    if response is None:
                        logging.error(f"Handler for {route_path} returned None")
                        return Response("500 Internal Server Error", status=500)
                    return response  # Return the response
                else:
                    # Method not allowed
                    logging.warning(f"Method {method} not allowed for {route_path}")
                    return Response("405 Method Not Allowed", status=405)

        # Route not found
        logging.warning(f"404 Not Found: {method} {path}")
        return Response("404 Not Found", status=404)