from flask import Blueprint, render_template, request
from datetime import datetime

from database.models.livro import Livro
from database.models.editora import Editora

livro_route = Blueprint('livro', __name__)

# /livros/ (GET) - listar os livros
@livro_route.route('/')
def lista_livros():
    livros = Livro.select().order_by(Livro.id)
    
    # atribuindo filtros do request para variáveis
    filtro_titulo = request.args.get("filtro_titulo", "").strip()
    filtro_autor = request.args.get("filtro_autor", "").strip()
    filtro_isbn = request.args.get("filtro_isbn", "").strip()
    filtro_editora = request.args.get("filtro_editora", "").strip()
    filtro_inicio = request.args.get("filtro_inicio", "").strip()
    filtro_fim = request.args.get("filtro_fim", "").strip()
    
    # testando se existem os filtros e adicionando-os a query de listagem
    if filtro_titulo:
        livros = livros.where(Livro.titulo.contains(filtro_titulo))
    
    if filtro_autor:
        livros = livros.where(Livro.autor.contains(filtro_autor))
    
    if filtro_isbn:
        livros = livros.where(Livro.ISBN.contains(filtro_isbn))
    
    if filtro_editora:
        livros = livros.where(Livro.editora.contains(filtro_editora))
        
    if filtro_inicio:
        try:
            data_inicio = datetime.strptime(filtro_inicio, '%Y-%m-%d')
            livros = livros.where(Livro.data_lancamento >= data_inicio)
        except ValueError:
            pass # se a data não estiver na formatação correta não realiza o filtro
    
    if filtro_fim:
        try:
            data_fim = datetime.strptime(filtro_fim, '%Y-%m-%d')
            livros = livros.where(Livro.data_lancamento <= data_fim)
        except ValueError:
            pass # se a data não estiver na formatação correta não realiza o filtro
                
    return render_template('livro/lista-livros.html', livros = livros)

# /livros/ (POST) - inserir livro no servidor
@livro_route.route('/', methods = ['POST'])
def inserir_livro():     
    dados = request.json # atribuindo os dados do request para uma variável
    
    # criando livro no banco de dados
    data = datetime.strptime(dados['dataLancamento'], "%Y-%m-%d") # transforma string em datetime
        
    novo_livro = Livro.create(
        titulo = dados['tituloLivro'],
        autor = dados['autorLivro'],
        editora = dados['editoraLivro'],
        ISBN = dados['ISBN'],
        data_lancamento = data
    )
        
    return render_template('livro/item_livro.html', livro = novo_livro)
    
# /livros/new (GET) - renderizar formulario de criação do livro
@livro_route.route('/new')
def form_livro():
    return render_template('livro/cadastro-livro.html', editoras = Editora.select())

# /livros/<id> (GET) - obter os dados de um livro
@livro_route.route('/<int:id>')
def detalhe_livro(id):
    livro = Livro.get_by_id(id)
    return render_template('livro/detalhe-livro.html', livro = livro)

# /livros/<id>/edit (GET) - renderizar formulário da edição do livro
@livro_route.route('/<int:id>/edit')
def editar_livro(id):
    livro = Livro.get_by_id(id)
    return render_template("livro/cadastro-livro.html", livro = livro)

# /livros/<id>/update (PUT) - atualizar os dados do livro
@livro_route.route('/<int:id>/update', methods = ['PUT'])
def atualizar_livro(id):
    dados = request.json
    
    data = datetime.strptime(dados['dataLancamento'], "%Y-%m-%d") # transforma string em datetime
    
    livro_editado = Livro.get_by_id(id)
    livro_editado.titulo = dados['tituloLivro']
    livro_editado.autor = dados['autorLivro']
    livro_editado.editora = dados['editoraLivro']
    livro_editado.ISBN = dados['ISBN']
    livro_editado.data_lancamento = data
    
    livro_editado.save()
    
    return render_template('livro/item_livro.html', livro = livro_editado)

# /livros/<id>/delete (DELETE) - deleta o registro do livro
@livro_route.route('/<int:id>/delete', methods = ['DELETE'])
def deletar_livro(id):
    livro_deletado = Livro.get_by_id(id)
    livro_deletado.delete_instance()
    
    return {'delete': 'ok'}