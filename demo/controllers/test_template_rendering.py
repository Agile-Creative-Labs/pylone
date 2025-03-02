"""
Jinja2 Template Rendering Example.

This script demonstrates how to use the Jinja2 templating engine to load and
render an HTML template. It sets up a Jinja2 environment, loads a template
from the file system, renders it with provided context data, and prints the
resulting HTML output.

Imports:
    jinja2.Environment: The Jinja2 environment class.
    jinja2.FileSystemLoader: The Jinja2 file system loader class.
    jinja2.select_autoescape: The Jinja2 autoescape function.

Usage:
    - Ensure the 'templates' directory exists in the parent directory of this script.
    - Ensure the 'private/dashboard.html' template exists within the 'templates' directory.
    - Run the script to render the template and print the output.


"""
from jinja2 import Environment, FileSystemLoader, select_autoescape
#TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../templates/")
# Set up the Jinja2 environment
env = Environment(
    loader=FileSystemLoader('../templates'),  # Adjust this path to point to your templates directory
    autoescape=select_autoescape(['html', 'xml'])
)

# Render the dashboard template
template = env.get_template('private/dashboard.html')
rendered = template.render({"title": "Dashboard", "user": {"id": 1, "username": "JohnDoe"}})
print(rendered)
