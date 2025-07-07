# Pylone Framework
Pylone is a lightweight, custom Python MVC (Model-View-Controller) framework designed to help you build web applications quickly and efficiently. It provides a simple yet powerful structure for organizing your code, handling routing, managing middleware, and serving static files

## Features

- MVC Architecture: Clean separation of concerns with Models, Views, and Controllers.
- Routing: Easy-to-define routes for handling HTTP requests.
- Middleware Support: Flexible middleware system for request/response processing.
- Static File Serving: Built-in support for serving static files (CSS, JS, images).
- Configuration Management: Centralized configuration system for environment-specific settings.
- Extensible: Easily extendable with custom middleware, controllers, and models.
- Jinja2 Engine
- Built-in Sockets, Ajax support

## Getting Started

Prerequisites

Python 3.7 or higher and pip (Python package manager)
## Installation
1.Git Clone
```sh
git clone https://github.com/your-username/pylone.git
cd pylone
```
2.Install dependencies:

```sh
pip install -r requirements.txt
```

## Running the Demo App
1.Navigate to the demo directory:
```sh
cd demo
cd pylone
```
2.Run the application
```sh
python3 run.py --port 8000 --ws-port 8001 --debug
```
2.Open your browser and navigate to 
```sh
http://localhost:8000
```
## **Directory Structure**
```
pylone/
├── demo/                      # Demo application
│   ├── app.py                 # Main application setup
│   ├── routes.py              # Route definitions
│   ├── controllers/           # Controllers for handling requests
│   ├── middlewares/           # Middleware for request/response processing
│   ├── models/                # Database models
│   ├── static/                # Static files (CSS, JS, images)
│   ├── templates/             # HTML templates
│   └── settings.py            # Application configuration
├── pylone/                    # Core framework
│   ├── __init__.py
│   ├── app.py                 # Core application logic
│   ├── router.py              # Routing logic
│   └── settings.py            # Default framework configuration
└── run.py                     # Script to run the application
```
## Configuration
The framework uses a centralized configuration system. You can define environment-specific settings in demo/settings.py.
Example Configuration:
```sh
import os
from pylone.settings import Config
class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME = os.getenv('DB_NAME', 'demo.db')
    DATABASE_URI = f"sqlite:///{DB_NAME}"
```
## Environment Variables
You can override settings using environment variables. For example:
```sh
export DB_NAME="my_database.db"
```
## Usage
### Defining Routes
Routes are defined in demo/routes.py. Example:
```sh
from demo.controllers.auth_controller import auth_controller
from demo.controllers.dashboard_controller import dashboard_controller

router = {
    '/login': auth_controller.login,
    '/dashboard': dashboard_controller.index,
}
```
### Creating Controllers
Controllers handle HTTP requests. Example:
```sh
class AuthController:
    def login(self, request):
        return "Login Page"
auth_controller = AuthController()
```
### Defining Middleware
Middleware can be used to process requests and responses. Example:
```sh
class AuthController:
    def login(self, request):
        return "Login Page"
auth_controller = AuthController()
```
### Serving static files
Static files are served from the static/ directory. Example:
```sh
<link rel="stylesheet" href="/static/css/styles.css">
<script src="/static/js/scripts.js"></script>
<img src="/static/images/logo.png" alt="Logo">
```
## Contributing
Contributions are welcome! If you'd like to contribute to Pylone, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your branch.
4. Submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
Inspired by Flask and Django.
Built with ❤️ by [Agile Creative Labs Inc.]

## Contact
For questions or feedback, feel free to reach out:
Email: pylone@agilecreativelabs.com




