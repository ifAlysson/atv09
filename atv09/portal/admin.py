from django.contrib import admin
from .models import Conteudo, Menu, GrupoMenu

# Register your models here.
admin.site.register(Conteudo)
admin.site.register(GrupoMenu)
admin.site.register(Menu)
