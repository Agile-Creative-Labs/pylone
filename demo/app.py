# demo/app.py
from pylone.app import App
from demo.routes import router

app = App()
app.setup(router)

# Debugging: Print registered routes
print("Debug: Routes registered in demo/app.py")
for path, route in router.routes.items():
    print(f"  - {path} -> {route['handler'].__name__}")




