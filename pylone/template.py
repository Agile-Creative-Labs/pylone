""" pylone/template.py

"""
import os
import re
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Set up logging
logging.basicConfig(level=logging.DEBUG)

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

        template = self.env.get_template(template_name)
        return template.render(context)
