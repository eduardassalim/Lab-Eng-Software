from flask import Blueprint, render_template, request
from datetime import datetime

from database.models.livro import Livro

livro_route = Blueprint('livro', __name__)

# /livros/ (GET) - listar os livros
@livro_route.route('/')
def lista_livros():
    return render_template('livro/lista-livros.html', livros = Livro.select().order_by(Livro.id))

# /livros/ (POST) - inserir livro no servidor
@livro_route.route('/', methods = ['POST'])
def inserir_livro():     
    dados = request.json # atribuindo os dados do request para uma variável
    
    # criando livro no banco de dados
    data = datetime.strptime(dados['dataLancamento'], "%Y-%m-%d") # transforma string em datetime
        
    novo_livro = Livro.create(
        titulo = dados['tituloLivro'],
        autor = dados['autorLivro'],
        ISBN = dados['ISBN'],
        data_lancamento = data
    )
        
    return render_template('livro/item_livro.html', livro = novo_livro)
    
# /livros/new (GET) - renderizar formulario de criação do livro
@livro_route.route('/new')
def form_livro():
    return render_template('livro/cadastro-livro.html')

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