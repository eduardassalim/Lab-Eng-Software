from flask import Blueprint, render_template, request

from database.models.editora import Editora

editora_route = Blueprint('editora', __name__)

# /editoras/ (GET) - listar as editoras
@editora_route.route('/')
def lista_editoras():
    editoras = Editora.select().order_by(Editora.id)
    
    # atribuindo filtros do request para variáveis
    filtro_nome = request.args.get("filtro_nome", "").strip()
    filtro_endereco = request.args.get("filtro_endereco", "").strip()
    filtro_telefone = request.args.get("filtro_telefone", "").strip()
    filtro_cnpj = request.args.get("filtro_cnpj", "").strip()
    
    # testando se existem os filtros e adicionando-os a query de listagem
    if filtro_nome:
        editoras = editoras.where(Editora.nome.contains(filtro_nome))
    
    if filtro_endereco:
        editoras = editoras.where(Editora.endereco.contains(filtro_endereco))
    
    if filtro_telefone:
        editoras = editoras.where(Editora.telefone.contains(filtro_telefone))
    
    if filtro_cnpj:
        editoras = editoras.where(Editora.CNPJ.contains(filtro_cnpj))
        
    return render_template('editora/lista-editoras.html', editoras = editoras)

# /editoras/ (POST) - inserir editora no servidor
@editora_route.route('/', methods = ['POST'])
def inserir_editora():     
    dados = request.json # atribuindo os dados do request para uma variável
    
    # criando editora no banco de dados        
    nova_editora = Editora.create(
        nome = dados['nomeEditora'],
        endereco = dados['endereco'],
        telefone = dados['telefoneEditora'],
        CNPJ = dados['cnpjEditora']
    )
    
    return render_template('editora/item_editora.html', editora = nova_editora)
    
# /editoras/new (GET) - renderizar formulario de criação de editora
@editora_route.route('/new')
def form_editora():
    return render_template('editora/cadastro-editora.html')

# /editoras/<id> (GET) - obter os dados de uma editora
@editora_route.route('/<int:id>')
def detalhe_editora(id):
    editora = Editora.get_by_id(id)
    return render_template('editora/detalhe-editora.html', editora = editora)

# /editoras/<id>/edit (GET) - renderizar formulário da edição da editora
@editora_route.route('/<int:id>/edit')
def editar_editora(id):
    editora = Editora.get_by_id(id)
    return render_template("editora/cadastro-editora.html", editora = editora)

# /editoras/<id>/update (PUT) - atualizar os dados da editora
@editora_route.route('/<int:id>/update', methods = ['PUT'])
def atualizar_editora(id):
    dados = request.json
    
    editora_editada = Editora.get_by_id(id)
    editora_editada.nome = dados['nomeEditora']
    editora_editada.endereco = dados['enderecoEditora']
    editora_editada.telefone = dados['telefoneEditora']
    editora_editada.CNPJ = dados['cnpjEditora']
    
    editora_editada.save()
    
    return render_template('editora/item_editora.html', editora = editora_editada)

# /editoras/<id>/delete (DELETE) - deleta o registro da editora
@editora_route.route('/<int:id>/delete', methods = ['DELETE'])
def deletar_editora(id):
    editora_deletado = Editora.get_by_id(id)
    editora_deletado.delete_instance()
    
    return {'delete': 'ok'}