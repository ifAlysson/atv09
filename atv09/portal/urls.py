from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='menu'),
    path('conteudo/<slug:slug>/', views.exibir_conteudo, name='conteudo'),
    path('grupos/<int:grupo_id>/alternar/', views.alternar_grupo, name='alternar_grupo'),
    path('ouvidoria/', views.ouvidoria, name='ouvidoria'),
    path('ouvidoria/sucesso/', views.ouvidoria_sucesso, name='ouvidoria_sucesso'),
]
