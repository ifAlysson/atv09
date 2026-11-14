# Portal V, A, J — Atividade 09

Projeto desenvolvido com **Python e Django**, dando continuidade ao site estático da atividade 07. O portal apresenta os conteúdos cadastrados no banco de dados, gera a navegação automaticamente e inclui a ouvidoria com formulário e tela de confirmação.

## 1. Requisitos

- Python 3.12, 3.13 ou 3.14 (compatível com a versão Django 6.1.2 definida no projeto);
- pip;
- Navegador atualizado.

As dependências Python estão listadas em `requirements.txt`.

## 2. Instalação

Abra um terminal na pasta `atv09` (a pasta que contém `manage.py`). Recomenda-se criar um ambiente virtual.

### Ubuntu / Debian

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r ../requirements.txt
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r ..\requirements.txt
```

> Caso o terminal já esteja na pasta raiz do repositório, entre em `atv09` antes de executar os comandos do Django.

## 3. Banco de dados e execução

Ainda dentro da pasta `atv09`, execute:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse:

- Portal: <http://127.0.0.1:8000/>
- Administração: <http://127.0.0.1:8000/admin/>
- Ouvidoria: <http://127.0.0.1:8000/ouvidoria/>
- Confirmação da ouvidoria: <http://127.0.0.1:8000/ouvidoria/sucesso/>

A migração `0011_ouvidoria_menu_e_capa_dinamica` cria o conteúdo e o botão da ouvidoria, corrige o vínculo do currículo da Jordana e substitui os botões antigos da capa por uma apresentação compatível com a navegação Django.

## 4. Como administrar os conteúdos e botões

Entre no Django Admin usando o superusuário criado.

### Conteúdo (`Conteudo`)

Cada página interna deve ter:

- **Título:** nome que será apresentado na capa;
- **Slug:** identificador usado na URL, por exemplo `curriculo-vinicius`;
- **Conteúdo:** HTML que será exibido na página;
- **Ativo:** define se a página pode ser acessada;
- **Capa:** marca o conteúdo que será mostrado na página inicial. O banco limita a existência de uma única capa.

Todo `Conteudo` ativo, exceto a própria capa, aparece automaticamente como um cartão com botão na página inicial. Portanto, para adicionar ou remover opções da capa, basta criar, ativar, desativar ou excluir os registros correspondentes no Admin. Não é necessário editar `index.html`.

O HTML salvo no campo **Conteúdo** é renderizado como HTML. Cadastre nesse campo apenas conteúdo confiável.

### Grupos (`GrupoMenu`) e botões (`Menu`)

- Crie um `GrupoMenu` para representar um controlador, como “Currículos” ou “Temas”.
- Crie registros `Menu` e selecione o grupo no campo **Controlador** para que os botões apareçam dentro dele.
- Deixe **Controlador** vazio para que o botão apareça diretamente na barra lateral.
- Para destino **Interno**, selecione um `Conteudo`.
- Para destino **Externo**, informe uma URL completa, começando por `https://`.
- Use os campos **Ordem** para organizar os itens. A ordem dos menus e a ordem dos grupos são configuradas separadamente.
- Desmarque **Ativo** para ocultar um grupo ou botão sem excluí-lo.

O formulário de administração valida o destino: um botão interno precisa de um conteúdo, e um botão externo precisa de uma URL. Botões sem destinos válidos também não são exibidos na navegação.

Os controladores são montados automaticamente pelo template com base nos registros relacionados no banco de dados. Ao clicar em um controlador, o estado aberto/fechado é guardado na sessão do visitante e permanece ao navegar entre páginas.

## 5. Ouvidoria

A ouvidoria possui duas telas:

1. `/ouvidoria/`: formulário com nome, e-mail, telefone, assunto, perfil e mensagem;
2. `/ouvidoria/sucesso/`: confirmação apresentada após o envio válido.

O formulário valida os campos no servidor. Após o envio, o Django guarda temporariamente o nome e o e-mail na sessão para personalizar a confirmação e redireciona para a página de sucesso. **Nesta versão acadêmica, a mensagem não é enviada por e-mail nem gravada permanentemente no banco de dados**, pois o projeto não possui um modelo de solicitações nem configuração de serviço de e-mail.

## 6. Arquivos importantes

```text
atv09/
├── atv09/                 # Configurações e URLs do projeto Django
├── portal/
│   ├── forms.py            # Formulário da ouvidoria
│   ├── migrations/         # Migrações do banco
│   ├── models.py           # Conteudo, GrupoMenu e Menu
│   ├── static/             # CSS e imagens
│   ├── templates/          # Layout, capa, conteúdo e ouvidoria
│   ├── urls.py             # Rotas da aplicação
│   └── views.py            # Capa, conteúdo, menu e ouvidoria
├── db.sqlite3              # Banco SQLite incluído no projeto
└── manage.py               # Comandos do Django
```

## 7. Testes

Dentro da pasta `atv09`, execute:

```bash
python manage.py test portal
python manage.py check
```

Os testes cobrem a geração dinâmica dos botões da capa, acesso a conteúdo pelo slug, persistência dos grupos na sessão, validação do formulário e redirecionamento para a tela de sucesso.

## 8. Observações

- O tema escolhido é mantido entre páginas usando o armazenamento local do navegador.
- Os arquivos CSS e imagens do site ficam em `portal/static/`.
- O banco usado por padrão é SQLite (`db.sqlite3`).
- Para parar o servidor de desenvolvimento, pressione `Ctrl + C` no terminal.
