from flask import Flask, render_template, request, redirect
from datetime import datetime
from database.models.cliente import Cliente
from database.models.atendente import Atendente
from database.models.livro import Livro
from database.models.editora import Editora
from database.database import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cadastro-cliente", methods = ['GET','POST'])
def cad_cliente():
    error = False
    error_message = None
    
    if (request.method == 'POST'):
        dados = request.form
                
        for cliente in Cliente.select():
            if cliente.email == dados['emailCliente']:
                error = True
        
        if (error != True):
            Cliente.create(
                nome = dados['nomeCliente'],
                email = dados['emailCliente'],
                telefone = dados['telefoneCliente']
            )
                        
            return redirect("/test-tables")
        else:
            error_message = "E-mail já existente!"
    return render_template('cadastro-clientes.html', error_message = error_message)

@app.route("/cadastro-livro", methods = ['GET', 'POST'])
def cad_livro():
    error = False
    error_message = None
    
    if (request.method == 'POST'):
        dados = request.form

        for livro in Livro.select():
            if livro.ISBN == dados['ISBN']:
                error = True
        
        if (error != True):
            data = datetime.strptime(dados['dataLancamento'], "%Y-%m-%d") # transforma string em datetime
            
            Livro.create(
                titulo = dados['tituloLivro'],
                autor = dados['autorLivro'],
                ISBN = dados['ISBN'],
                data_lancamento = data
            )
                             
            return redirect("/test-tables")
        else:
            error_message = "ISBN para livro já cadastrado!"
    
    return render_template('cadastro-livro.html', error_message = error_message)

@app.route("/cadastro-atendente", methods = ['GET', 'POST'])
def cad_atendente():
    error = False
    error_message = None
    
    if (request.method == 'POST'):
        dados = request.form
        
        for atendente in Atendente.select():
            if atendente.email == dados['emailAtendente']:
                error = True
        
        if (error != True):
            Atendente.create(
                nome = dados['nomeAtendente'],
                email = dados['emailAtendente'],
                cargo = dados['cargo']
            )
                        
            return redirect("/test-tables")
        else:
            error_message = "E-mail já cadastrado!"
            
    return render_template('cadastro-atendente.html', error_message = error_message)

@app.route("/cadastro-editora", methods = ['GET', 'POST'])
def cad_editora():
    error = False
    error_message = None
    
    if (request.method == 'POST'):
        dados = request.form
        
        for editora in Editora.select():
            if editora.CNPJ == dados['cnpjEditora']:
                error = True
        
        if (error != True):
            Editora.create(
                nome = dados['nomeEditora'],
                endereco = dados['endereco'],
                telefone = dados['telefoneEditora'],
                CNPJ = dados['cnpjEditora']
            )
                        
            return redirect("/test-tables")
        else:
            error_message = "CNPJ já cadastrado!"
    
    return render_template('cadastro-editora.html', error_message = error_message)

@app.route("/test-tables")
def test_tables():
    return render_template('test-tables.html', clientes = Cliente.select(), atendentes = Atendente.select(), editoras = Editora.select(), livros = Livro.select())

db.connect()

db.create_tables([Cliente, Atendente, Livro, Editora])

if (__name__ == '__main__'):
    app.run(debug=True)