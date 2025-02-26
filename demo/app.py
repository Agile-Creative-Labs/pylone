# demo/app.py
from pylone.app import App
from demo.routes import router
from demo.middlewares.logging_middleware import LoggingMiddleware
from demo.middlewares.auth_middleware import AuthMiddleware

# Create the app with middlewares
#app = App(router, middlewares=[LoggingMiddleware])
# Create the app with middlewares
app = App(router, middlewares=[LoggingMiddleware, AuthMiddleware])
app.setup(router)