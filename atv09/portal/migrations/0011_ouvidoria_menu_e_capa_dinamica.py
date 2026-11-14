from django.db import migrations
from django.db.models import Max


CONTEUDO_CAPA_ATUALIZADO = '''
<div class="apresentacao-capa">
    <img src="/static/img/welcome.jpg" alt="Boas-vindas ao site V, A, J" class="imagem-boas-vindas">
    <h1>Bem-vindo ao nosso espaço!</h1>
    <p>Explore os conteúdos dos integrantes e conheça um pouco mais sobre cada um de nós.</p>
</div>
'''


def criar_ouvidoria_e_corrigir_links(apps, schema_editor):
    Conteudo = apps.get_model('portal', 'Conteudo')
    Menu = apps.get_model('portal', 'Menu')
    db_alias = schema_editor.connection.alias

    ouvidoria, _ = Conteudo.objects.using(db_alias).get_or_create(
        slug='ouvidoria',
        defaults={
            'titulo': 'Ouvidoria',
            'conteudo': '<p>Use o formulário para enviar sua mensagem.</p>',
            'ativo': True,
            'capa': False,
        },
    )

    menu_ouvidoria = Menu.objects.using(db_alias).filter(titulo='Ouvidoria').first()
    if menu_ouvidoria is None:
        maior_ordem = Menu.objects.using(db_alias).aggregate(maior=Max('ordem'))['maior']
        menu_ouvidoria = Menu(
            titulo='Ouvidoria',
            nome_exibicao='Ouvidoria',
            tipo_destino='interno',
            conteudo_relacionado=ouvidoria,
            ordem=(maior_ordem if maior_ordem is not None else -1) + 1,
            ativo=True,
        )
    else:
        menu_ouvidoria.nome_exibicao = 'Ouvidoria'
        menu_ouvidoria.tipo_destino = 'interno'
        menu_ouvidoria.conteudo_relacionado = ouvidoria
        menu_ouvidoria.url_externo = None
        menu_ouvidoria.ativo = True
    menu_ouvidoria.save(using=db_alias)

    # Corrige o vínculo incorreto que apontava o currículo da Jordana para o do Vinícius.
    curriculo_jordana = Conteudo.objects.using(db_alias).filter(slug='curriculo_jordana').first()
    menu_jordana = Menu.objects.using(db_alias).filter(titulo__icontains='Jordana').first()
    if curriculo_jordana and menu_jordana:
        menu_jordana.conteudo_relacionado = curriculo_jordana
        menu_jordana.save(using=db_alias, update_fields=['conteudo_relacionado'])

    # Remove do HTML antigo os botões estáticos que chamavam funções JavaScript inexistentes.
    capa = Conteudo.objects.using(db_alias).filter(slug='capa').first()
    if capa and capa.conteudo and 'carregarConteudo(' in capa.conteudo:
        capa.conteudo = CONTEUDO_CAPA_ATUALIZADO
        capa.save(using=db_alias, update_fields=['conteudo'])


def reverter_dados(apps, schema_editor):
    # Mantém os dados caso a migração seja revertida; eles podem ter sido editados no Admin.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('portal', '0010_grupomenu_nome_exibicao_menu_nome_exibicao_and_more'),
    ]

    operations = [
        migrations.RunPython(criar_ouvidoria_e_corrigir_links, reverter_dados),
    ]
