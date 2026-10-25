from django.db import models

class Conteudo(models.Model):
	titulo = models.CharField(max_length=100, null=True)
	slug = models.SlugField(unique=True, null=True)
	conteudo = models.TextField(null=True, help_text='Insira o HTML interno da nova página')
	ativo = models.BooleanField(default=True)
	capa = models.BooleanField(default=False, help_text='Defina a página inicial (máx. 1)')

	def __str__(self):
		return self.titulo

	class Meta:
                constraints = [
                        models.UniqueConstraint(fields=['capa'], condition=models.Q(capa=True), name='apenas_uma_capa')
                        ]

class GrupoMenu(models.Model):
	titulo = models.CharField(max_length=100, null=True)
	nome_exibicao = models.CharField(max_length=100, help_text='Defina o nome que será exibido no menu lateral', default='Botão')
	ordem = models.PositiveIntegerField(unique=True, default=0, help_text='Define a ordem dos botões')
	ativo = models.BooleanField(default=True)

	def __str__(self):
		return self.titulo

	class Meta:
		ordering = ['ordem']

class Menu(models.Model):
    opcoes = (('interno', 'Interno'), ('externo', 'Externo'))

    titulo = models.CharField(max_length=100, null=True)
    nome_exibicao = models.CharField(max_length=100, help_text='Defina o nome que será exibido no menu lateral', default='Botão')
    tipo_destino = models.CharField(max_length=20, choices=opcoes, default='interno')
    conteudo_relacionado = models.ForeignKey(Conteudo, on_delete=models.CASCADE, null=True, blank=True)
    url_externo = models.URLField(max_length=200, null=True, help_text='Link para acessar site externo', default=None, blank=True)
    ordem = models.PositiveIntegerField(unique=True, default=0, help_text='Define a ordem dos botões')
    ativo = models.BooleanField(default=True)
    controlador = models.ForeignKey(GrupoMenu, on_delete=models.SET_NULL, null=True, blank=True, help_text='Selecione o botão controlador, não selecione nehum para que fique independente')

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return self.titulo
    
    def tipo(self):
        return self.tipo
