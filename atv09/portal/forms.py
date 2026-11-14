from django import forms
from django.core.validators import RegexValidator


class OuvidoriaForm(forms.Form):
    """Formulário de contato usado pela ouvidoria da atividade 07."""

    ASSUNTOS = (
        ('duvida', 'Dúvida'),
        ('sugestao', 'Sugestão'),
        ('critica', 'Crítica'),
        ('reportarerro', 'Reportar erro'),
    )

    PERFIS = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('comunidade', 'Comunidade externa'),
    )

    nome = forms.CharField(
        label='Nome completo',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'caixaformulario', 'autocomplete': 'name'}),
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'caixaformulario', 'autocomplete': 'email'}),
    )
    telefone = forms.CharField(
        label='Telefone',
        min_length=11,
        max_length=11,
        validators=[RegexValidator(r'^\d{11}$', 'Informe os 11 números do telefone, incluindo o DDD.')],
        widget=forms.TextInput(attrs={
            'class': 'caixaformulario',
            'inputmode': 'numeric',
            'pattern': '[0-9]{11}',
            'placeholder': '82999999999',
        }),
    )
    assunto = forms.ChoiceField(
        label='Assunto',
        choices=ASSUNTOS,
        widget=forms.Select(attrs={'class': 'caixaformulario'}),
    )
    perfil = forms.ChoiceField(
        label='Perfil do usuário',
        choices=PERFIS,
        widget=forms.RadioSelect,
    )
    mensagem = forms.CharField(
        label='Mensagem',
        min_length=15,
        widget=forms.Textarea(attrs={'class': 'caixaformulario', 'rows': 5}),
    )
