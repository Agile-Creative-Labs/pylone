from pylone.router import Router
from pylone.request import Request
from pylone.response import Response
from pylone.template import TemplateEngine

app = Router()
template_engine = TemplateEngine("demo/templates")

def form_page(request):
    return Response(template_engine.render("form.html"))

def result_page(request):
    name = request.query_params.get("name", [""])[0]
    return Response(template_engine.render("result.html", {"user_name": name}))

app.add_route("/", form_page)
app.add_route("/result", result_page, methods=['GET'])



