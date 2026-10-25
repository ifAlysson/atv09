from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Conteudo, Menu, GrupoMenu


def obter_botoes():
    """Retorna uma lista com instâncias ativas de Menu e tuplas no fomarto (GrupoMenu, [subordinados ao GrupoMenu]).
Todo botão que tiver um controlador é retornado como um item de uma lista numa tupla cujo primeiro índice é o controlador e o segundo os controlados.
Na saída, a lista contém essas tuplas e botões independentes, então cuidado com a mistura de tipos na saída.
A saída é ordenada mesclando a ordem dos botões normais e controladores em O(N^2)."""

    """Retorna uma lista com instâncias de Menu e GrupoMenu organizadas corretamente para o Django HTML criar os botões na ordem e divisão de grupos correta"""

    botoes_acesso = Menu.objects.all()
    
    elementos = list()
    controladores = dict()
    for botao in botoes_acesso:
        # Percorre todos os botões de acesso
        if botao.ativo:
            # Nos que estiverem ativos...
            if botao.controlador is not None and botao.controlador.ativo:
                # ... veja se ele tem um controlador ativo. Se tiver, adicione em controladores...
                controladores.setdefault(botao.controlador, []).append(botao)
                """try:
                    controladores[botao.controlador].append(botao)
                except KeyError:
                    controladores[botao.controlador] = [botao]"""
            else:
                # ... se não tiver, adicione em elementos.
                elementos.append(botao)

    # Adicione todos os controladores em elementos no formato (controlador, [controlados])
    for controlador in controladores.keys():
        elementos.append((controlador, controladores[controlador]))

    # Este bubble sort ordena os botões mesclando a ordem dos botões normais e dos controladores
    # Como é possível que um normal e um controlador tenham o mesmo valor na ordem, o controlador fica sempree depois de um normal nesse caso
    ordenado = False
    while not ordenado:
        ordenado = True
        # Descobre as ordens dos dois elementos, tratando a diferença de tipos da lista
        for i in range(len(elementos) - 1):
            try:
                ordemi1 = elementos[i].ordem
            except:
                ordemi1 = elementos[i][0].ordem
            try:
                ordemi2 = elementos[i + 1].ordem
            except:
                ordemi2 = elementos[i + 1][0].ordem

            if ordemi1 == ordemi2: #Identifica um normal e um controlador sendo comparados
                if type(elementos[i]) is tuple: # Identifica que o controlador vem antes, logo está desordenado
                    ordenado = False
                    aux = elementos[i] #OBS: USAR [:] ??
                    elementos[i] = elementos[i + 1]
                    elementos[i + 1] = aux
            else: #Identifica dois elementos do mesmo tipo sendo comparados
                if ordemi1 > ordemi2: # Se a primeira ordem for maior que a segunda, está desordenado
                    ordenado = False
                    aux = elementos[i] #OBS IDEM!!
                    elementos[i] = elementos[i + 1]
                    elementos[i + 1] = aux

    saida = []
    for elemento in elementos:
        if type(elemento) is tuple:
            saida.append(elemento[0])
            for botao in elemento[1]:
                saida.append(botao)
        else:
            saida.append(elemento)
    
    return saida


def index(request):
    """Define o conteúdo interno que será exibido como capa. Apresenta duas mensagens de erro: uma para quando há elementos, mas nenhuma capa definida, e outra para quando não há nenhum elemento.
O erro é retornado como HTML exibido dentro do portal"""

    conteudos = Conteudo.objects.all()
    botoes = obter_botoes()
    if len(conteudos) == 0:
        capa = {
            'conteudo' : '<p> <b>ERRO</b>: Você não criou nenhuma página interna.<br>Crie uma acessando o <a target="_blank" href="http://127.0.0.1:8000/admin">Django Admin</a>.<br>Lembre-se de criar um super usuário para acessar a administração.</p>'
                }
    else:
        capa = None
        for cont in conteudos:
            if cont.capa:
                capa = cont
                break
        if capa is None:
            capa = {
                'conteudo' : '<p> <b>ERRO</b>: Você não definiu nenhuma página para ser a capa padrão.<br>Defina uma acessando o <a target="_blank" href="http://127.0.0.1:8000/admin">Django Admin</a>.<br>Lembre-se de criar um super usuário para acessar a administração.</p>'
                }
    template = loader.get_template('index.html')
    context = {
        'capa' : capa,
        'botoes' : botoes,
    }
    
    return HttpResponse(template.render(context, request))
                

"""def obter_elementos_menu():
	botoes_conteudo = Menu.objects.all()
	botoes_controle = Menu.objects.all()

        elementos = list()
        controladores = dict()
        
	for botao in botoes_conteudo:
                if type(botao)"""






















def obter_elementos_menu2():
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

        # Ordena os botões internos usando Bubble Sort
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

    # Ordena grupos e botões independentes por ordem
    n = len(elementos)

    for i in range(n):
        for j in range(n - i - 1):
            a = elementos[j]
            b = elementos[j + 1]

            ordem_a = a['objeto'].ordem
            ordem_b = b['objeto'].ordem

            trocar = ordem_a > ordem_b

            # Em caso de empate, o grupo vem primeiro
            if ordem_a == ordem_b:
                if a['tipo'] == 'botao' and b['tipo'] == 'grupo':
                    trocar = True

            if trocar:
                elementos[j], elementos[j + 1] = (
                    elementos[j + 1],
                    elementos[j]
                )

    return elementos


def menu_view(request):
    return render(request, 'layout.html', {
        'elementos_menu': obter_elementos_menu(),
        'conteudo_atual': None,
        'grupo_aberto': None,
    })


def exibir_conteudo(request, slug):
    conteudo = get_object_or_404(
        Conteudo,
        slug=slug,
        ativo=True
    )

    # Descobre qual botão do menu leva a este conteúdo.
    botao_atual = Menu.objects.filter(
        conteudo_relacionado=conteudo,
        ativo=True
    ).first()

    # Descobre o grupo controlador desse botão, se houver.
    grupo_aberto = None

    if botao_atual and botao_atual.controlador_id is not None:
        grupo_aberto = botao_atual.controlador_id

    return render(request, 'conteudo.html', {
        'conteudo': conteudo,
        'elementos_menu': obter_elementos_menu(),
        'conteudo_atual': conteudo,
        'grupo_aberto': grupo_aberto,
    })
