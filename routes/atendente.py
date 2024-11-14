from flask import Blueprint, render_template, request

from database.models.atendente import Atendente

atendente_route = Blueprint('atendente', __name__)

# /atendentes/ (GET) - listar os atendentes
@atendente_route.route('/')
def lista_atendentes():
    return render_template('atendente/lista-atendentes.html', atendentes = Atendente.select().order_by(Atendente.id))

# /atendentes/ (POST) - inserir atendente no servidor
@atendente_route.route('/', methods = ['POST'])
def inserir_atendente():     
    dados = request.json # atribuindo os dados do request para uma variável
    
    # criando atendente no banco de dados        
    novo_atendente = Atendente.create(
        nome = dados['nomeAtendente'],
        email = dados['emailAtendente'],
        cargo = dados['cargoAtendente']
    )
        
    return render_template('atendente/item_atendente.html', atendente = novo_atendente)
    
# /atendentes/new (GET) - renderizar formulario de criação do atendente
@atendente_route.route('/new')
def form_atendente():
    return render_template('atendente/cadastro-atendente.html')

# /atendentes/<id> (GET) - obter os dados de um atendente
@atendente_route.route('/<int:id>')
def detalhe_atendente(id):
    atendente = Atendente.get_by_id(id)
    return render_template('atendente/detalhe-atendente.html', atendente=atendente)

# /atendentes/<id>/edit (GET) - renderizar formulário da edição do atendente
@atendente_route.route('/<int:id>/edit')
def editar_atendente(id):
    atendente = Atendente.get_by_id(id)
    return render_template("atendente/cadastro-atendente.html", atendente = atendente)

# /atendentes/<id>/update (PUT) - atualizar os dados do atendente
@atendente_route.route('/<int:id>/update', methods = ['PUT'])
def atualizar_atendente(id):
    dados = request.json
    
    atendente_editado = Atendente.get_by_id(id)
    atendente_editado.nome = dados['nomeAtendente']
    atendente_editado.email = dados['emailAtendente']
    atendente_editado.cargo = dados['cargoAtendente']
    
    atendente_editado.save()
    
    return render_template('atendente/item_atendente.html', atendente=atendente_editado)

# /atendentes/<id>/delete (DELETE) - deleta o registro do atendente
@atendente_route.route('/<int:id>/delete', methods = ['DELETE'])
def deletar_atendente(id):
    atendente_deletado = Atendente.get_by_id(id)
    atendente_deletado.delete_instance()
    
    return {'delete': 'ok'}