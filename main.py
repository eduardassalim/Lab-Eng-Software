from flask import Flask, render_template, request, redirect # importação dos métodos Flask utilizados no código

from datetime import datetime # importação do método datetime

# importação das models das tabelas do banco (abaixo)
from database.models.cliente import Cliente
from database.models.atendente import Atendente
from database.models.livro import Livro
from database.models.editora import Editora

from database.database import db # importação do banco de dados

app = Flask(__name__) # inicialização padrão do aplicativo Flask

# rota raiz
@app.route("/")
def index():
    return render_template('index.html')

# rota para o cadastro do cliente
@app.route("/cadastro-cliente", methods = ['GET','POST'])
def cad_cliente():
    error = False
    error_message = None # inicialização de variáveis para verificar erro
    
    if (request.method == 'POST'): # verificando se o método do rerquest está sendo um POST
        dados = request.form # atribuindo os dados do request de uma tag for para uma variável
                
        # verificando se o email do request já está cadastrado no banco de dados
        for cliente in Cliente.select():
            if cliente.email == dados['emailCliente']:
                error = True
        
        # se não houver erro irá realizar a inserção no banco de dados
        if (error != True):
            Cliente.create(
                nome = dados['nomeCliente'],
                email = dados['emailCliente'],
                telefone = dados['telefoneCliente']
            )
                        
            return redirect("/test-tables") # redirecionamento para outra página
        
        # em caso de erro, uma mensagem de erro é renderizada com o template para realizar o cadastro novamente
        else:
            error_message = "E-mail já existente!"
    return render_template('cadastro-clientes.html', error_message = error_message)

#rota para o cadastro do livro
@app.route("/cadastro-livro", methods = ['GET', 'POST']) # definido os dois métodos de request da página
def cad_livro():
    error = False
    error_message = None # inicialização de variáveis para verificar erro
    
    if (request.method == 'POST'): # verificando se o método do rerquest está sendo um POST
        dados = request.form # atribuindo os dados do request de uma tag for para uma variável

        # verificando se a ISBN do request já está cadastrada no banco de dados
        for livro in Livro.select():
            if livro.ISBN == dados['ISBN']:
                error = True
        
        # se não houver erro irá realizar a inserção no banco de dados
        if (error != True):
            data = datetime.strptime(dados['dataLancamento'], "%Y-%m-%d") # transforma string em datetime
            
            Livro.create(
                titulo = dados['tituloLivro'],
                autor = dados['autorLivro'],
                ISBN = dados['ISBN'],
                data_lancamento = data
            )
                             
            return redirect("/test-tables") # redirecionamento para outra página
        
        # em caso de erro, uma mensagem de erro é renderizada com o template para realizar o cadastro novamente
        else:
            error_message = "ISBN para livro já cadastrado!"
    
    return render_template('cadastro-livro.html', error_message = error_message) 

@app.route("/cadastro-atendente", methods = ['GET', 'POST'])
def cad_atendente():
    error = False
    error_message = None # em caso de erro, uma mensagem de erro é renderizada com o template para realizar o cadastro novamente
    
    # verificando se o método do rerquest está sendo um POST
    if (request.method == 'POST'):
        dados = request.form # atribuindo os dados do request de uma tag for para uma variável
        
        # verificando se o email do request já está cadastrado no banco de dados
        for atendente in Atendente.select():
            if atendente.email == dados['emailAtendente']:
                error = True
        
        # se não houver erro irá realizar a inserção no banco de dados
        if (error != True):
            Atendente.create(
                nome = dados['nomeAtendente'],
                email = dados['emailAtendente'],
                cargo = dados['cargo']
            )
                        
            return redirect("/test-tables") # redirecionamento para outra página
        
        # em caso de erro, uma mensagem de erro é renderizada com o template para realizar o cadastro novamente
        else:
            error_message = "E-mail já cadastrado!"
            
    return render_template('cadastro-atendente.html', error_message = error_message)

# rota para cadastro de editora
@app.route("/cadastro-editora", methods = ['GET', 'POST'])
def cad_editora():
    error = False
    error_message = None # inicialização de variáveis para verificar erro
    
    # verificando se o método do rerquest está sendo um POST
    if (request.method == 'POST'):
        dados = request.form # atribuindo os dados do request de uma tag for para uma variável
        
        # verificando se o CNPJ do request já está cadastrado no banco de dados
        for editora in Editora.select():
            if editora.CNPJ == dados['cnpjEditora']:
                error = True
        
        # se não houver erro irá realizar a inserção no banco de dados
        if (error != True):
            Editora.create(
                nome = dados['nomeEditora'],
                endereco = dados['endereco'],
                telefone = dados['telefoneEditora'],
                CNPJ = dados['cnpjEditora']
            )
            
            return redirect("/test-tables") # redirecionamento para outra página
        
        # em caso de erro, uma mensagem de erro é renderizada com o template para realizar o cadastro novamente
        else:
            error_message = "CNPJ já cadastrado!"
    
    return render_template('cadastro-editora.html', error_message = error_message)

# rota para a tela de listagem dos dados do banco de dados
@app.route("/test-tables")
def test_tables():
    return render_template('test-tables.html', clientes = Cliente.select(), atendentes = Atendente.select(), editoras = Editora.select(), livros = Livro.select())

db.connect() # conexão com o banco de dados

db.create_tables([Cliente, Atendente, Livro, Editora]) # criação das tabelas do banco de dados (caso as tabelas já existirem ele irá carrega-las)

# verifica se o programa está sendo rodado no main e roda a aplicação Flask
if (__name__ == '__main__'):
    app.run(debug=True)