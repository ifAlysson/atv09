from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='menu'),
    #('conteudo/<slug:slug>/', views.exibir_conteudo, name='conteudo'),
]
