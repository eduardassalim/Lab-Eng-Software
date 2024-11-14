from flask import Flask, render_template, request, redirect # importação dos métodos Flask utilizados no código

from datetime import datetime # importação do método datetime

from routes.home import home_route # importação da blueprint home
from routes.cliente import cliente_route # importação da blueprint cliente
from routes.atendente import atendente_route # importação da blueprint atendente
from routes.editora import editora_route # importação da blueprint editora
from routes.livro import livro_route # importação da blueprint editora

# importação das models das tabelas do banco (abaixo)
from database.models.livro import Livro
from database.models.cliente import Cliente
from database.models.editora import Editora
from database.models.atendente import Atendente

from database.database import db # importação do banco de dados

app = Flask(__name__) # inicialização padrão do aplicativo Flask

app.register_blueprint(home_route)
app.register_blueprint(cliente_route, url_prefix='/clientes')
app.register_blueprint(atendente_route, url_prefix='/atendentes')
app.register_blueprint(editora_route, url_prefix='/editoras')
app.register_blueprint(livro_route, url_prefix='/livros')

db.connect() # conexão com o banco de dados

db.create_tables([Cliente, Atendente, Livro, Editora]) # criação das tabelas do banco de dados (caso as tabelas já existirem ele irá carrega-las)

# verifica se o programa está sendo rodado no main e roda a aplicação Flask
if (__name__ == '__main__'):
    app.run(debug=True)