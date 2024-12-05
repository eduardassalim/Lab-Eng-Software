from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime, timedelta

from database.models.livro import Livro
from database.models.cliente import Cliente
from database.models.emprestimo import Emprestimo
from database.models.avaliacao import Avaliacao

emprestimo_route = Blueprint('emprestimo', __name__)

# /emprestimos/ (GET) - carregar a página principal dos emprestimos
@emprestimo_route.route('/')
def home_emprestimos():
    return render_template('emprestimo/home-emprestimo.html')

# /emprestimos/list (GET) - listar os emprestimos
@emprestimo_route.route('/list')
def lista_emprestimos():
    emprestimos = Emprestimo.select().order_by(Emprestimo.id)
    
    # atribuindo filtros do request para variáveis
    filtro_cliente = request.args.get("filtro_cliente", "").strip()
    filtro_inicio_emprestimo = request.args.get("filtro_inicio_emprestimo", "").strip()
    filtro_fim_emprestimo = request.args.get("filtro_fim_emprestimo", "").strip()
    filtro_inicio_registro = request.args.get("filtro_inicio_registro", "").strip()
    filtro_fim_registro = request.args.get("filtro_fim_registro", "").strip()
    
    # testando se existem os filtros e adicionando-os a query de listagem
    if filtro_cliente:
        emprestimos = emprestimos.where(Emprestimo.cliente.contains(filtro_cliente))
        
    if filtro_inicio_emprestimo:
        try:
            data_inicio = datetime.strptime(filtro_inicio_emprestimo, '%Y-%m-%d')
            emprestimos = emprestimos.where(Emprestimo.data_emprestimo >= data_inicio)
        except ValueError:
            pass # se a data não estiver na formatação correta não realiza o filtro
    
    if filtro_fim_emprestimo:
        try:
            data_fim = datetime.strptime(filtro_fim_emprestimo, '%Y-%m-%d')
            emprestimos = emprestimos.where(Emprestimo.data_emprestimo <= data_fim)
        except ValueError:
            pass # se a data não estiver na formatação correta não realiza o filtro
        
    if filtro_inicio_registro:
        try:
            data_inicio = datetime.strptime(filtro_inicio_registro, '%Y-%m-%d')
            emprestimos = emprestimos.where(Emprestimo.data_registro >= data_inicio)
        except ValueError:
            pass # se a data não estiver na formatação correta não realiza o filtro
    
    if filtro_fim_registro:
        try:
            data_fim = datetime.strptime(filtro_fim_registro, '%Y-%m-%d')
            emprestimos = emprestimos.where(Emprestimo.data_registro <= data_fim)
        except ValueError:
            pass # se a data não estiver na formatação correta não realiza o filtro
                
    return render_template('emprestimo/lista-emprestimos.html', emprestimos = emprestimos)

# /emprestimos/ (POST) - inserir emprestimo no servidor
@emprestimo_route.route('/', methods = ['POST'])
def inserir_emprestimo():     
    dados = request.json # atribuindo os dados do request para uma variável
    
    # criando emprestimo no banco de dados
    datetime_emprestimo = datetime.strptime(dados['dataEmprestimo'], "%d/%m/%Y") if dados['dataEmprestimo'] else datetime.now() # transforma string em datetime
    datetime_devolucao = datetime.strptime(dados['dataDevolucao'], "%d/%m/%Y") if dados['dataDevolucao'] else datetime_emprestimo + timedelta(days=7) # adiciona 7 dias com base na data de empréstimo
        
    novo_emprestimo = Emprestimo.create(
        cliente = dados['idCliente'],
        livro = dados['idLivro'],
        data_emprestimo = datetime_emprestimo,
        data_devolucao = datetime_devolucao 
    )
    
    # atualiza a disponibilidade do livro para False
    livro = Livro.get_or_none(Livro.id == dados['idLivro'])
    livro.disponivel = False
    livro.save()
        
    return render_template('emprestimo/item_emprestimo.html', emprestimo = novo_emprestimo)

# /emprestimos/<id>/return (POST) - realizar a devolução do empréstimo
@emprestimo_route.route('/<int:id>/return', methods=['POST'])
def devolver_emprestimo(id):
    emprestimo = Emprestimo.get_or_none(Emprestimo.id == id)

    # Atualizar a disponibilidade do livro para True
    livro = emprestimo.livro
    livro.disponivel = True
    livro.save()

    # atualiza a data de devolução para o momento atual
    emprestimo.data_devolucao = datetime.now()
    emprestimo.save()

    # atualiza a situação do empréstimo
    emprestimo.devolvido = True
    emprestimo.save()

    return redirect(url_for('emprestimo.home_emprestimos'))

# /emprestimos/new (GET) - renderizar formulario de criação do emprestimo
@emprestimo_route.route('/new')
def form_emprestimo():
    # filtrando apenas os livros disponíveis
    livros = [livro for livro in Livro.select() if livro.disponivel]
    
    return render_template('emprestimo/cadastro-emprestimo.html', livros = livros, clientes = Cliente.select())

# /emprestimos/<id> (GET) - obter os dados de um emprestimo
@emprestimo_route.route('/<int:id>')
def detalhe_emprestimo(id):
    emprestimo = Emprestimo.get_by_id(id)
    
    # busca a avaliação associada ao empréstimo
    avaliacao_existente = Avaliacao.get_or_none(Avaliacao.emprestimo == emprestimo)
    
    # calcula a média das avaliações do livro
    avaliacoes = Avaliacao.select().where(Avaliacao.livro == emprestimo.livro)
    media_avaliacoes = sum(avaliacao.nota for avaliacao in avaliacoes) / avaliacoes.count() if avaliacoes else None
    
    return render_template('emprestimo/detalhe-emprestimo.html', emprestimo = emprestimo, avaliacao_existente = avaliacao_existente, media_avaliacoes = media_avaliacoes, quantidade_avaliacoes = avaliacoes.count() if avaliacoes else 0)

# /emprestimos/<id>/edit (GET) - renderizar formulário da edição do emprestimo
@emprestimo_route.route('/<int:id>/edit')
def editar_emprestimo(id):
    clientes = Cliente.select()
    livros = Livro.select()
    emprestimo = Emprestimo.get_by_id(id)
    return render_template("emprestimo/cadastro-emprestimo.html", emprestimo = emprestimo, clientes = clientes, livros = livros)

# /emprestimos/<id>/update (PUT) - atualizar os dados do emprestimo
@emprestimo_route.route('/<int:id>/update', methods = ['PUT'])
def atualizar_emprestimo(id):
    dados = request.json
    
    datetime_emprestimo = datetime.strptime(dados['dataEmprestimo'], "%d/%m/%Y") # transforma string em datetime
    datetime_devolucao = datetime.strptime(dados['dataDevolucao'], "%d/%m/%Y") # transforma string em datetime
    
    emprestimo_editado = Emprestimo.get_by_id(id)
    emprestimo_editado.cliente = dados['idCliente'],
    emprestimo_editado.livro = dados['idLivro'],
    emprestimo_editado.data_emprestimo = datetime_emprestimo,
    emprestimo_editado.data_devolucao = datetime_devolucao or datetime_emprestimo + timedelta(days=7) # adiciona 7 dias com base na data de empréstimo
    
    emprestimo_editado.save()
    
    return render_template('emprestimo/item_emprestimo.html', emprestimo = emprestimo_editado)

# /emprestimos/<id>/delete (DELETE) - deleta o registro do emprestimo
@emprestimo_route.route('/<int:id>/delete', methods = ['DELETE'])
def deletar_emprestimo(id):
    emprestimo_deletado = Emprestimo.get_by_id(id)
    emprestimo_deletado.delete_instance()
    
    return {'delete': 'ok'}