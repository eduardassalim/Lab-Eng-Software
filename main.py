from flask import Flask, render_template, request, redirect
from db import CLIENTES, ATENDENTES, EDITORAS, LIVROS
from datetime import datetime

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
                
        for cliente in CLIENTES:
            if cliente['email'] == dados['emailCliente']:
                error = True
        
        if (error != True):
            novoCliente = {
                "id": (CLIENTES[len(CLIENTES) - 1]["id"] + 1),
                "nome": dados['nomeCliente'],
                "email": dados['emailCliente'],
                "telefone": dados['telefoneCliente']
            }
            
            CLIENTES.append(novoCliente)
            
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

        for livro in LIVROS:
            if livro['titulo'] == dados['tituloLivro']:
                error = True
        
        if (error != True):
            data = datetime.strptime(dados['dataLancamento'], "%Y-%m-%d")

            novoLivro = {
                "id": (LIVROS[len(LIVROS) - 1]["id"] + 1),
                "titulo": dados['tituloLivro'],
                "autor": dados['autorLivro'],
                "ISBN": dados['ISBN'],
                "dataLancamento": data.strftime("%d/%m/%Y")
            }
            
            LIVROS.append(novoLivro)
            
            return redirect("/test-tables")
        else:
            error_message = "Título para livro já cadastrado!"
    
    return render_template('cadastro-livro.html', error_message = error_message)

@app.route("/cadastro-atendente", methods = ['GET', 'POST'])
def cad_atendente():
    error = False
    error_message = None
    
    if (request.method == 'POST'):
        dados = request.form
        
        for atendente in ATENDENTES:
            if atendente['email'] == dados['emailAtendente']:
                error = True
        
        if (error != True):
            novoAtendente = {
                "id": (ATENDENTES[len(ATENDENTES) - 1]["id"] + 1),
                "nome": dados['nomeAtendente'],
                "email": dados['emailAtendente'],
                "cargo": dados['cargo']
            }
            
            ATENDENTES.append(novoAtendente)
            
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
        
        for editora in EDITORAS:
            if editora['CNPJ'] == dados['cnpjEditora']:
                error = True
        
        if (error != True):
            novaEditora = {
                "id": (EDITORAS[len(EDITORAS) - 1]["id"] + 1),
                "nome": dados['nomeEditora'],
                "endereco": dados['endereco'],
                "telefone": dados['telefoneEditora'],
                "CNPJ": dados['cnpjEditora']
            }
            
            EDITORAS.append(novaEditora)
            
            return redirect("/test-tables")
        else:
            error_message = "CNPJ já cadastrado!"
    
    return render_template('cadastro-editora.html', error_message = error_message)

@app.route("/test-tables")
def test_tables():
    return render_template('test-tables.html', clientes = CLIENTES, atendentes = ATENDENTES, editoras = EDITORAS, livros = LIVROS)

if (__name__ == '__main__'):
    app.run(debug=True)