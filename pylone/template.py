import os

class TemplateEngine:
    def __init__(self, template_dir):
        self.template_dir = template_dir

    def render(self, template_name, context={}):
        """Loads and renders an HTML template with context variables."""
        template_path = os.path.join(self.template_dir, template_name)

        if not os.path.exists(template_path):
            return f"Template '{template_name}' not found."

        with open(template_path, "r") as file:
            content = file.read()

        for key, value in context.items():
            content = content.replace("{{ " + key + " }}", str(value))

        return content
    
    def render_template(template, context):
        with open(template, "r") as file:
            content = file.read()
            for key, value in context.items():
                content = content.replace(f"{{{{ {key} }}}}", str(value))
            return content