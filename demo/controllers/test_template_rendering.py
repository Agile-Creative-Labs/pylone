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
