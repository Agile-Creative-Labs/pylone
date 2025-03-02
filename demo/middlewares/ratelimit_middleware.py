"""
Rate Limiting Middleware for a Python WSGI Application.

This module provides a middleware class, RateLimitingMiddleware, that wraps a WSGI
application to limit the number of requests from a specific client IP within a
defined time window. It prevents excessive requests and protects against
brute-force attacks.

Imports:
    time: For handling timestamps and time-related operations.
    collections.defaultdict: For creating dictionaries with default values.
    logging: For logging messages (not used in current code, but can be added for logging rate limiting events).

Classes:
    RateLimitingMiddleware: A WSGI middleware that limits request rates.

Functions:
    None.
 * Author: Agile Creative Labs Inc.
 * Version: 1.0.0
 * Date: 02/23/2024
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