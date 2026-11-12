from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Conteudo, Menu, GrupoMenu


def obter_botoes():
    """Retorna uma lista com instâncias ativas de Menu e tuplas no fomarto (GrupoMenu, [subordinados ao GrupoMenu]).
Todo botão que tiver um controlador é retornado como um item de uma lista numa tupla cujo primeiro índice é o controlador e o segundo os controlados.
A saída é ordenada mesclando a ordem dos botões normais e controladores em O(N^2).
Retorna uma lista com instâncias de Menu e GrupoMenu organizadas corretamente para o Django HTML criar os botões na ordem e divisão de grupos correta"""

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






