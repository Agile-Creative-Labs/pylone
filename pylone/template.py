""" pylone/template.py

"""
import os
import logging
import re
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Set up logging
logging.basicConfig(level=logging.INFO)

class TemplateEngine:
    def __init__(self, templates_dir):
        """Initialize the Jinja2 template environment."""
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render(self, template_name, context=None):
        """Render a template with the given context."""
        if context is None:
            context = {}

        try:
            template = self.env.get_template(template_name)
            return template.render(context)
        except Exception as e:
            logging.error(f"Template rendering error: {e}")
            raise

    def render_template(self, template_name, context=None, status=200, headers=None):
        """Render a template and return a WSGI-compliant response."""
        try:
            template = self.env.get_template(template_name)
            body = template.render(**(context or {}))
            headers = headers or {}
            headers['Content-Type'] = 'text/html'
            return body, status, headers
        except Exception as e:
            logging.error(f"Template rendering error: {e}")
            raise