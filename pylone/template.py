"""pylone/template.py

This module provides a TemplateEngine class for rendering Jinja2 templates.

It encapsulates the Jinja2 environment setup, allowing for easy template
loading and rendering with optional context. It also includes methods for
generating WSGI-compliant responses from rendered templates, suitable for
web applications.

Key features:
    - Initialization of a Jinja2 Environment with file system loader and autoescaping.
    - Template rendering with context handling and error logging.
    - Generation of WSGI-compliant responses with rendered template content.

Usage:
    Initialize a TemplateEngine with a directory containing templates:
    >>> engine = TemplateEngine("templates")

    Render a template with a context:
    >>> rendered_output = engine.render("index.html", {"name": "User"})

    Generate a WSGI-compliant response:
    >>> body, status, headers = engine.render_template("page.html", {"data": "content"})
    
    Date Created: February 26, 2025
    Author: alex@agilecreativelabs.ca
    Copyright: © 2025 Agile Creative Labs Inc.
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