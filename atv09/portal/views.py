from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import OuvidoriaForm
from .models import Conteudo, GrupoMenu, Menu


SESSION_GRUPOS_ABERTOS = 'grupos_menu_abertos'


def obter_itens_menu(request):
    """Monta o menu lateral a partir dos registros ativos do banco.

    Cada item retornado é um botão independente ou um grupo controlador com
    seus respectivos botões subordinados. A ordem dos dois tipos de item é
    respeitada, e grupos sem botões válidos não são exibidos.
    """
    grupos_abertos = request.session.get(SESSION_GRUPOS_ABERTOS, {})
    if not isinstance(grupos_abertos, dict):
        grupos_abertos = {}

    grupos = {
        grupo.pk: {
            'tipo': 'grupo',
            'grupo': grupo,
            'botoes': [],
            'aberto': bool(grupos_abertos.get(str(grupo.pk), False)),
            'ordem': grupo.ordem,
        }
        for grupo in GrupoMenu.objects.filter(ativo=True)
    }

    elementos = []
    menus = Menu.objects.filter(ativo=True).select_related(
        'conteudo_relacionado', 'controlador'
    ).order_by('ordem')

    for menu in menus:
        # Não cria links internos sem uma página ativa, nem links externos vazios.
        if menu.tipo_destino == 'interno':
            if not menu.conteudo_relacionado or not menu.conteudo_relacionado.ativo:
                continue
            if menu.conteudo_relacionado.capa:
                continue
        elif menu.tipo_destino == 'externo':
            if not menu.url_externo:
                continue
        else:
            continue

        grupo = grupos.get(menu.controlador_id)
        if grupo is not None:
            grupo['botoes'].append(menu)
        else:
            elementos.append({
                'tipo': 'menu',
                'menu': menu,
                'ordem': menu.ordem,
                'desempate': 0,
            })

    for grupo in grupos.values():
        if grupo['botoes']:
            elementos.append({**grupo, 'desempate': 1})

    # Em caso de empate, o botão independente aparece antes do controlador.
    elementos.sort(key=lambda item: (item['ordem'], item['desempate']))
    return elementos


def contexto_layout(request, pagina_atual=None):
    return {
        'itens_menu': obter_itens_menu(request),
        'pagina_atual': pagina_atual,
    }


def index(request):
    """Exibe a capa e gera seus botões com base nos conteúdos ativos."""
    capa = Conteudo.objects.filter(ativo=True, capa=True).first()
    conteudos_capa = Conteudo.objects.filter(
        ativo=True,
    ).exclude(capa=True).exclude(slug__isnull=True).exclude(slug='').order_by('titulo')

    if capa is None:
        mensagem_erro = (
            '<p><strong>ERRO:</strong> Nenhuma página foi definida como capa. '
            'Acesse o Django Admin e marque um conteúdo como capa.</p>'
        )
        capa = {'conteudo': mensagem_erro}

    contexto = {
        **contexto_layout(request, 'capa'),
        'capa': capa,
        'conteudos_capa': conteudos_capa,
    }
    return render(request, 'index.html', contexto)


def exibir_conteudo(request, slug):
    """Exibe um conteúdo pelo slug, respeitando as páginas especiais."""
    conteudo = get_object_or_404(Conteudo, slug=slug, ativo=True)

    if conteudo.capa:
        return redirect('menu')
    if conteudo.slug == 'ouvidoria':
        return redirect('ouvidoria')

    contexto = {
        **contexto_layout(request, conteudo.slug),
        'conteudo': conteudo,
    }
    return render(request, 'conteudo.html', contexto)


@require_POST
def alternar_grupo(request, grupo_id):
    """Alterna e guarda na sessão o estado aberto/fechado de um grupo."""
    grupo = get_object_or_404(GrupoMenu, pk=grupo_id, ativo=True)
    estados = request.session.get(SESSION_GRUPOS_ABERTOS, {})
    if not isinstance(estados, dict):
        estados = {}

    chave = str(grupo.pk)
    estados[chave] = not bool(estados.get(chave, False))
    request.session[SESSION_GRUPOS_ABERTOS] = estados

    destino = request.POST.get('next') or reverse('menu')
    if not url_has_allowed_host_and_scheme(
        url=destino,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        destino = reverse('menu')
    return redirect(destino)


def ouvidoria(request):
    """Recebe o formulário da atividade 07 e encaminha à tela de sucesso."""
    if request.method == 'POST':
        form = OuvidoriaForm(request.POST)
        if form.is_valid():
            # A atividade original apenas confirma o envio; não há envio de e-mail
            # nem armazenamento permanente porque o projeto não possui esse modelo.
            request.session['ouvidoria_confirmacao'] = {
                'nome': form.cleaned_data['nome'],
                'email': form.cleaned_data['email'],
            }
            return redirect('ouvidoria_sucesso')
    else:
        form = OuvidoriaForm()

    contexto = {
        **contexto_layout(request, 'ouvidoria'),
        'form': form,
    }
    return render(request, 'ouvidoria.html', contexto)


def ouvidoria_sucesso(request):
    confirmacao = request.session.pop('ouvidoria_confirmacao', None)
    contexto = {
        **contexto_layout(request, 'ouvidoria'),
        'confirmacao': confirmacao,
    }
    return render(request, 'ouvidoria_sucesso.html', contexto)
