from django.db import models

class Conteudo(models.Model):
	nome = models.CharField(max_length=100, null=True)
	slug = models.SlugField(unique=True, null=True)
	conteudo = models.TextField(null=True)
	ativo = models.BooleanField(default=False)

	def __str__(self):
		return self.nome
