from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Conteudo, GrupoMenu, Menu


class PortalViewsTests(TestCase):
    def setUp(self):
        self.capa = Conteudo.objects.create(
            titulo='Capa de teste',
            slug='capa_teste',
            conteudo='<h1>Bem-vindo</h1>',
            ativo=True,
            capa=True,
        )
        self.pagina = Conteudo.objects.create(
            titulo='Página de teste',
            slug='pagina-teste',
            conteudo='<p>Conteúdo dinâmico de teste.</p>',
            ativo=True,
            capa=False,
        )

    def test_capa_exibe_botoes_dos_conteudos_ativos(self):
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Página de teste')
        self.assertContains(response, reverse('conteudo', args=['pagina-teste']))

    def test_conteudo_interno_abre_pelo_slug(self):
        response = self.client.get(reverse('conteudo', args=['pagina-teste']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Conteúdo dinâmico de teste.')

    def test_grupo_aberto_permanece_aberto_ao_navegar(self):
        grupo = GrupoMenu.objects.create(
            titulo='Grupo de teste',
            nome_exibicao='Grupo de teste',
            ordem=50,
            ativo=True,
        )
        Menu.objects.create(
            titulo='Página do grupo',
            nome_exibicao='Página do grupo',
            tipo_destino='interno',
            conteudo_relacionado=self.pagina,
            ordem=50,
            ativo=True,
            controlador=grupo,
        )

        resposta_toggle = self.client.post(
            reverse('alternar_grupo', args=[grupo.pk]),
            {'next': reverse('menu')},
        )
        self.assertRedirects(resposta_toggle, reverse('menu'))
        self.assertTrue(self.client.session['grupos_menu_abertos'][str(grupo.pk)])

        resposta_pagina = self.client.get(reverse('conteudo', args=['pagina-teste']))
        self.assertEqual(resposta_pagina.status_code, 200)
        self.assertContains(resposta_pagina, 'Página do grupo')

    def test_ouvidoria_redireciona_para_sucesso_apos_envio_valido(self):
        dados = {
            'nome': 'Pessoa de Teste',
            'email': 'teste@example.com',
            'telefone': '82999999999',
            'assunto': 'sugestao',
            'perfil': 'aluno',
            'mensagem': 'Esta é uma mensagem de teste válida.',
        }
        response = self.client.post(reverse('ouvidoria'), dados, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1][0], reverse('ouvidoria_sucesso'))
        self.assertContains(response, 'Pessoa de Teste')
        self.assertContains(response, 'teste@example.com')

    def test_ouvidoria_nao_aceita_telefone_invalido(self):
        dados = {
            'nome': 'Pessoa de Teste',
            'email': 'teste@example.com',
            'telefone': '12345',
            'assunto': 'duvida',
            'perfil': 'aluno',
            'mensagem': 'Esta é uma mensagem de teste válida.',
        }
        response = self.client.post(reverse('ouvidoria'), dados)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Informe os 11 números do telefone')

    def test_botao_interno_nao_pode_ser_cadastrado_sem_conteudo(self):
        menu = Menu(
            titulo='Botão sem destino',
            nome_exibicao='Botão sem destino',
            tipo_destino='interno',
            conteudo_relacionado=None,
            ordem=99,
        )
        with self.assertRaises(ValidationError):
            menu.full_clean()
