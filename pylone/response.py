"""pylone/response.py

This module defines the Response class, which encapsulates HTTP responses for
a WSGI application. It handles various response body types, status codes,
headers, and cookies, and provides a method to convert the response to a
WSGI-compatible format.

Key features:
    - Initialization with body, status, headers, and cookies.
    - Automatic status message generation from status code.
    - Cookie handling and inclusion in headers.
    - JSON serialization for dictionary bodies.
    - String encoding for HTML or plain text bodies.
    - Support for iterable byte bodies.
    - Logging of response details.
    - Conversion to WSGI-compatible (status, headers, body) tuple.

Usage:
    Create a Response object:
    >>> response = Response("Hello, World!", status=200, headers={"Content-Type": "text/plain"})

    Create a JSON response:
    >>> response = Response({"message": "Success"}, status=200)

    Create a response with cookies:
    >>> response = Response("Cookie set!", status=200, cookies={"session_id": "12345"})

    Convert to WSGI format:
    >>> status, headers, body = response.to_wsgi()

    Date Created: February 26, 2025
    Author: alex@agilecreativelabs.ca
    Copyright: © 2025 Agile Creative Labs Inc.
"""
import logging
import json
from http import cookies

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Response:
    STATUS_MESSAGES = {
        200: "OK",
        201: "Created",
        204: "No Content",
        301: "Moved Permanently",
        302: "Found",
        304: "Not Modified",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        422: "Unprocessable Entity",
        429: "Too Many Requests",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
    }
    
    def __init__(self, body=None, status=200, headers=None, cookies=None):
        """
        Initialize a Response object.
        Args:
            body: The response body (str, dict, or iterable of bytes).
            status: The HTTP status code (int or str).
            headers: A dictionary or list of tuples representing HTTP headers.
            cookies: A dictionary of cookies to set in the response.
        """
        self.body = body
        self.status = f"{status} {self.STATUS_MESSAGES.get(status, 'Unknown')}" if isinstance(status, int) else status
        self.headers = list(headers.items()) if isinstance(headers, dict) else list(headers or [])
        self.cookies = cookies if cookies is not None else {}
        
    def set_cookie(self, name, value, **kwargs):
        """
        Set a cookie with the given name and value.
        
        Args:
            name: Cookie name
            value: Cookie value
            **kwargs: Additional cookie attributes (max_age, expires, path, domain, secure, httponly, samesite)
        """
        if self.cookies is None:
            self.cookies = {}
        
        self.cookies[name] = {"value": value, **kwargs}
        return self
    
    def add_header(self, name, value):
        """Add a header to the response."""
        self.headers.append((name, value))
        return self
    
    def json(self, data, status=200):
        """Create a JSON response."""
        self.body = data
        self.status = f"{status} {self.STATUS_MESSAGES.get(status, 'Unknown')}" if isinstance(status, int) else status
        self._ensure_content_type("application/json")
        return self
    
    def text(self, content, status=200):
        """Create a plain text response."""
        self.body = content
        self.status = f"{status} {self.STATUS_MESSAGES.get(status, 'Unknown')}" if isinstance(status, int) else status
        self._ensure_content_type("text/plain")
        return self
    
    def html(self, content, status=200):
        """Create an HTML response."""
        self.body = content
        self.status = f"{status} {self.STATUS_MESSAGES.get(status, 'Unknown')}" if isinstance(status, int) else status
        self._ensure_content_type("text/html")
        return self
    
    def redirect(self, location, status=302):
        """Create a redirect response."""
        self.body = f"Redirecting to {location}"
        self.status = f"{status} {self.STATUS_MESSAGES.get(status, 'Found')}" if isinstance(status, int) else status
        self.headers.append(("Location", location))
        return self
    
    def _ensure_content_type(self, content_type):
        """Ensure the Content-Type header is set."""
        for i, (name, value) in enumerate(self.headers):
            if name.lower() == "content-type":
                self.headers[i] = ("Content-Type", content_type)
                return
        self.headers.append(("Content-Type", content_type))
    
    def _format_cookie(self, name, value):
        """Format cookie header value according to RFC."""
        if isinstance(value, dict):
            cookie = cookies.SimpleCookie()
            cookie[name] = value.get("value", "")
            
            # Set cookie attributes
            if "max_age" in value:
                cookie[name]["max-age"] = value["max_age"]
            if "expires" in value:
                cookie[name]["expires"] = value["expires"]
            if "path" in value:
                cookie[name]["path"] = value["path"]
            if "domain" in value:
                cookie[name]["domain"] = value["domain"]
            if value.get("secure"):
                cookie[name]["secure"] = True
            if value.get("httponly"):
                cookie[name]["httponly"] = True
            if "samesite" in value:
                cookie[name]["samesite"] = value["samesite"]
                
            # Get the formatted cookie string without the "Set-Cookie: " prefix
            cookie_str = cookie.output(header="")
            return cookie_str.strip()
        else:
            return f"{name}={value}"
    
    def to_wsgi(self):
        """Convert the response to a WSGI-compatible format."""
        # Ensure headers is a list of tuples
        headers = self.headers.copy()
        
        # Add content type if not present
        has_content_type = any(name.lower() == "content-type" for name, _ in headers)
        if not has_content_type and self.body is not None:
            if isinstance(self.body, dict):
                headers.append(("Content-Type", "application/json"))
            elif isinstance(self.body, str):
                headers.append(("Content-Type", "text/html"))
        
        # Add cookies to headers
        for name, value in self.cookies.items():
            cookie_str = self._format_cookie(name, value)
            headers.append(("Set-Cookie", cookie_str))
        
        # Log response details
        logging.debug(f"Response status: {self.status}")
        logging.debug(f"Response headers: {headers}")
        logging.debug(f"Response cookies: {self.cookies}")
        
        # Handle body encoding
        try:
            if self.body is None:
                body = [b""]
            elif isinstance(self.body, dict):
                # Serialize JSON data
                body = [json.dumps(self.body).encode('utf-8')]
            elif isinstance(self.body, str):
                # Encode HTML or plain text
                body = [self.body.encode('utf-8')]
            elif isinstance(self.body, bytes):
                # Already bytes
                body = [self.body]
            elif hasattr(self.body, '__iter__'):
                # Assume body is already an iterable of bytes or strings
                body = [chunk.encode('utf-8') if isinstance(chunk, str) else chunk for chunk in self.body]
            else:
                # Convert to string and encode
                body = [str(self.body).encode('utf-8')]
        except (TypeError, ValueError) as e:
            logging.error(f"Error encoding response body: {e}", exc_info=True)
            body = [b"Internal Server Error"]
            
            # Update headers and status
            for i, (name, _) in enumerate(headers):
                if name.lower() == "content-type":
                    headers[i] = ("Content-Type", "text/plain")
                    break
            else:
                headers.append(("Content-Type", "text/plain"))
                
            self.status = "500 Internal Server Error"
        
        return self.status, headers, body