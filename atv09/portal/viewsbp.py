from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Conteudo, Menu, GrupoMenu

def layout(request):
	conteudos = Conteudo.objects.all().values()
	template = loader.get_template('layout.html')
	context = {
		'conteudos' : conteudos,
	}
	return HttpResponse(template.render(context, request))


def exibir_conteudo(request, slug):
    conteudo = get_object_or_404(
        Conteudo,
        slug=slug,
        ativo=True
    )

    return render(request, 'conteudo.html', {
        'conteudo': conteudo
    })

def menu_view(request):
    menus = list(Menu.objects.filter(ativo=True))
    grupos = list(GrupoMenu.objects.filter(ativo=True))

    elementos = []

    # Adiciona os botões independentes
    for menu in menus:
        if menu.controlador_id is None:
            elementos.append({
                'tipo': 'botao',
                'objeto': menu
            })

    # Adiciona os grupos e seus botões
    for grupo in grupos:
        botoes = [
            menu for menu in menus
            if menu.controlador_id == grupo.id
        ]

        # Ordena os botões do grupo por ordem (Bubble Sort)
        n = len(botoes)

        for i in range(n):
            for j in range(n - i - 1):
                if botoes[j].ordem > botoes[j + 1].ordem:
                    botoes[j], botoes[j + 1] = (
                        botoes[j + 1],
                        botoes[j]
                    )

        elementos.append({
            'tipo': 'grupo',
            'objeto': grupo,
            'botoes': botoes
        })

    # Ordena os grupos e botões independentes
    # por ordem, priorizando grupos em caso de empate
    n = len(elementos)

    for i in range(n):
        for j in range(n - i - 1):
            a = elementos[j]
            b = elementos[j + 1]

            ordem_a = a['objeto'].ordem
            ordem_b = b['objeto'].ordem

            trocar = ordem_a > ordem_b

            if ordem_a == ordem_b:
                if a['tipo'] == 'botao' and b['tipo'] == 'grupo':
                    trocar = True

            if trocar:
                elementos[j], elementos[j + 1] = (
                    elementos[j + 1],
                    elementos[j]
                )

    return render(request, 'layout.html', {
        'elementos_menu': elementos
    })
