"""

Usage:

demo/app.py

    from demo.middlewares.rate_limiting_middleware import RateLimitingMiddleware
    # Create the app with middlewares
    app = App(router, middlewares=[LoggingMiddleware, RateLimitingMiddleware])
"""
import time
from collections import defaultdict
import logging
class RateLimitingMiddleware:
    def __init__(self, app, max_requests=100, time_window=60):
        """
        Initialize the rate-limiting middleware.

        Args:
            app: The WSGI application to wrap.
            max_requests: Maximum number of requests allowed in the time window.
            time_window: Time window in seconds.
        """
        self.app = app
        self.max_requests = max_requests
        self.time_window = time_window
        self.request_counts = defaultdict(list)

    def __call__(self, environ, start_response):
        """Middleware interface: makes the middleware callable."""
        client_ip = environ.get("REMOTE_ADDR")

        # Remove old requests
        current_time = time.time()
        self.request_counts[client_ip] = [
            timestamp for timestamp in self.request_counts[client_ip]
            if current_time - timestamp < self.time_window
        ]

        # Check if the client has exceeded the limit
        if len(self.request_counts[client_ip]) >= self.max_requests:
            start_response("429 Too Many Requests", [("Content-Type", "text/plain")])
            return [b"Too many requests. Please try again later."]

        # Record the current request
        self.request_counts[client_ip].append(current_time)

        # Call the next middleware or the app
        return self.app(environ, start_response)