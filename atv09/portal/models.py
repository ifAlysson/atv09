from django.db import models

class Conteudo(models.Model):
	titulo = models.CharField(max_length=100, null=True)
	slug = models.SlugField(unique=True, null=True)
	conteudo = models.TextField(null=True)
	ativo = models.BooleanField(default=True)

	def __str__(self):
		return self.titulo


class Menu(models.Model):
    opcoes = [('interno', 'Interno'), ('externo', 'Externo')]

    titulo = models.CharField(max_length=100, null=True)
    tipo = models.CharField(max_length=20, choices=opcoes, default='interno')
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    def tipo(self):
        return self.tipo
