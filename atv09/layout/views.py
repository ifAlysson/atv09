from django.http import HttpResponse
from django.template import loader

def layout(request):
	template = loader.get_template('layout.html')
	return HttpResponse(template.render())
