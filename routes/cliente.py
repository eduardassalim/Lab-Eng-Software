from flask import Blueprint, render_template, request

from database.models.cliente import Cliente

cliente_route = Blueprint('cliente', __name__)

# /clientes/ (GET) - listar os clientes
@cliente_route.route('/')
def lista_clientes():
    return render_template('cliente/lista-clientes.html', clientes = Cliente.select().order_by(Cliente.id))

# /clientes/ (POST) - inserir cliente no servidor
@cliente_route.route('/', methods = ['POST'])
def inserir_cliente():
    error = False
        
    dados = request.json # atribuindo os dados do request para uma variável
    
    # verificando se o email do request já está cadastrado no banco de dados
    for cliente in Cliente.select():
        if cliente.email == dados['emailCliente']:
            error = True
                
    # se não houver erro irá realizar a inserção no banco de dados
    if not error:
        novo_cliente = Cliente.create(
            nome = dados['nomeCliente'],
            email = dados['emailCliente'],
            telefone = dados['telefoneCliente']
        )
        
    return render_template('cliente/item_cliente.html', cliente = novo_cliente)
    
# /clientes/new (GET) - renderizar formulario de criação do cliente
@cliente_route.route('/new')
def form_cliente():
    return render_template('cliente/cadastro-clientes.html')

# /clientes/<id> (GET) - obter os dados de um cliente
@cliente_route.route('/<int:id>')
def detalhe_cliente(id):
    cliente = Cliente.get_by_id(id)
    return render_template('cliente/detalhe-cliente.html', cliente=cliente)

# /clientes/<id>/edit (GET) - renderizar formulário da edição do cliente
@cliente_route.route('/<int:id>/edit')
def editar_cliente(id):
    cliente = Cliente.get_by_id(id)
    return render_template("cliente/cadastro-clientes.html", cliente = cliente)

# /clientes/<id>/update (PUT) - atualizar os dados do cliente
@cliente_route.route('/<int:id>/update', methods = ['PUT'])
def atualizar_cliente(id):
    dados = request.json
    
    cliente_editado = Cliente.get_by_id(id)
    cliente_editado.nome = dados['nomeCliente']
    cliente_editado.email = dados['emailCliente']
    cliente_editado.telefone = dados['telefoneCliente']
    
    cliente_editado.save()
    
    return render_template('cliente/item_cliente.html', cliente=cliente_editado)

# /clientes/<id>/delete (DELETE) - deleta o registro do cliente
@cliente_route.route('/<int:id>/delete', methods = ['DELETE'])
def deletar_cliente(id):
    cliente_deletado = Cliente.get_by_id(id)
    cliente_deletado.delete_instance()
    
    return {'delete': 'ok'}