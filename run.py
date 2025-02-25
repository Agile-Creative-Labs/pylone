from pylone.router import Router
from pylone.app import App
from pylone.response import Response

router = Router()

def hello_world(request):
    return Response("Hello, world!")

router.add_route("/", hello_world)

app = App(router)

# Now run the application
from wsgiref.simple_server import make_server

def application(environ, start_response):
    status, headers, body = app.handle_request(environ)
    start_response(f"{status} OK", headers)
    return body

server = make_server('localhost', 8000, application)
print("Serving on http://localhost:8000")
server.serve_forever()
