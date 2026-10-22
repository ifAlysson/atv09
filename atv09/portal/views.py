from django.http import HttpResponse
from django.template import loader
from .models import Conteudo

def layout(request):
	conteudos = Conteudo.objects.all().values()
	template = loader.get_template('layout.html')
	context = {
		'conteudos' : conteudos,
	}
	return HttpResponse(template.render(context, request))
