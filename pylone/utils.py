import html

def sanitize_input(input_data):
    """Sanitize user input to prevent XSS."""
    if isinstance(input_data, str):
        return html.escape(input_data)
    elif isinstance(input_data, dict):
        return {key: sanitize_input(value) for key, value in input_data.items()}
    elif isinstance(input_data, list):
        return [sanitize_input(item) for item in input_data]
    return input_data