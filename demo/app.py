# demo/app.py
from pylone.app import App
from demo.routes import router

# Create the app and set up the router
app = App()
app.setup(router)


