"""pylone/request.py

This module defines the Request class, which encapsulates HTTP request data
from a WSGI environment. It provides methods to access request method, path,
headers, cookies, and form data.

Key features:
    - Initialization from a WSGI environment dictionary.
    - Extraction of HTTP method and path.
    - Parsing of HTTP headers and cookies.
    - Parsing of form data from POST requests.
    - A 'get' method for retrieving form data values.

Usage:
    Create a Request object from a WSGI environment:
    >>> request = Request(environ)

    Access request attributes:
    >>> method = request.method
    >>> path = request.path
    >>> cookies = request.cookies
    >>> form_data = request.form_data

    Retrieve form data:
    >>> value = request.get('key', 'default_value')

    Date Created: December 12, 2024
    Author: cooper@agilecreativelabs.ca
    Copyright: © 2025 Agile Creative Labs Inc.
"""
import logging
import json
from urllib.parse import parse_qs

class Request:
    def __init__(self, environ):
        self.environ = environ
        self.method = environ.get('REQUEST_METHOD', 'GET')
        self.path = environ.get('PATH_INFO', '/')
        self.query_params = self._parse_query_params(environ.get('QUERY_STRING', ''))
        self.headers = self._parse_headers(environ)
        self.cookies = self._parse_cookies(environ.get('HTTP_COOKIE', ''))
        self.body = self._parse_body(environ)
        
        logging.debug(f"Request Path Extracted: {self.path}")
        logging.debug(f"Request Method: {self.method}")
        logging.debug(f"Request Headers: {self.headers}")
        logging.debug(f"Request Cookies: {self.cookies}")
        logging.debug(f"Request Query Params: {self.query_params}")
        logging.debug(f"Request Body: {self.body}")
    
    def _parse_query_params(self, query_string):
        """Parse query parameters from the URL."""
        return parse_qs(query_string)
    
    def _parse_headers(self, environ):
        """Parse headers from the environment."""
        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                header_name = key[5:].replace('_', '-').title()
                headers[header_name] = value
        return headers
    
    def _parse_cookies(self, cookie_header):
        """Parse cookies from the HTTP_COOKIE header."""
        cookies = {}
        if cookie_header:
            for cookie in cookie_header.split(';'):
                try:
                    key, value = cookie.strip().split('=', 1)
                    cookies[key] = value
                except ValueError:
                    logging.warning(f"Malformed cookie ignored: {cookie}")
        return cookies
    
    def _parse_body(self, environ):
        """Parse the request body based on the content type."""
        content_type = environ.get('CONTENT_TYPE', '')
        body = {}
        
        if self.method in ['POST', 'PUT', 'PATCH']:
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except ValueError:
                request_body_size = 0
                
            # Add size limit to prevent DoS attacks
            max_size = 10 * 1024 * 1024  # 10MB limit
            if request_body_size > max_size:
                logging.warning(f"Request body size ({request_body_size} bytes) exceeds limit")
                return body
                
            if request_body_size > 0:
                request_body = environ['wsgi.input'].read(request_body_size)
                try:
                    request_body = request_body.decode('utf-8')
                    if 'application/json' in content_type:
                        try:
                            body = json.loads(request_body)
                        except json.JSONDecodeError as e:
                            logging.error(f"Failed to parse JSON body: {e}")
                    elif 'application/x-www-form-urlencoded' in content_type:
                        body = parse_qs(request_body)
                except UnicodeDecodeError as e:
                    logging.error(f"Failed to decode request body: {e}")
        
        return body
    
    def get(self, key, default=None):
        """Retrieve a value from the query parameters or form data."""
        # Handle both list values and direct values
        if key in self.query_params:
            values = self.query_params.get(key)
            return values[0] if values else default
        elif key in self.body:
            if isinstance(self.body, dict) and isinstance(self.body.get(key), list):
                values = self.body.get(key)
                return values[0] if values else default
            return self.body.get(key, default)
        return default