import os
import mimetypes
from http import HTTPStatus

class StaticFileMiddleware:
    def __init__(self, app, static_dir='static'):
        self.app = app
        self.static_dir = static_dir

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        
        # Check if the request is for a static file
        if path.startswith('/static/'):
            file_path = os.path.join(self.static_dir, path[len('/static/'):])
            
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Serve the static file
                with open(file_path, 'rb') as file:
                    content = file.read()
                
                # Determine the MIME type
                mime_type, _ = mimetypes.guess_type(file_path)
                mime_type = mime_type or 'application/octet-stream'
                
                # Send response headers
                headers = [
                    ('Content-Type', mime_type),
                    ('Content-Length', str(len(content))),
                    ('Cache-Control', 'public, max-age=3600'),  # Cache for 1 hour
                ]
                start_response(f'{HTTPStatus.OK.value} {HTTPStatus.OK.phrase}', headers)
                return [content]
            else:
                # File not found
                start_response(f'{HTTPStatus.NOT_FOUND.value} {HTTPStatus.NOT_FOUND.phrase}', [])
                return [b'File Not Found']
        
        # Pass the request to the next middleware or app
        return self.app(environ, start_response)