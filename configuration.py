from database.database import db # importação do banco de dados

from routes.home import home_route # importação da blueprint home
from routes.cliente import cliente_route # importação da blueprint cliente
from routes.atendente import atendente_route # importação da blueprint atendente
from routes.editora import editora_route # importação da blueprint editora
from routes.livro import livro_route # importação da blueprint editora
from routes.emprestimo import emprestimo_route # importação da blueprint editora

# importação das models das tabelas do banco (abaixo)
from database.models.livro import Livro
from database.models.cliente import Cliente
from database.models.editora import Editora
from database.models.atendente import Atendente
from database.models.emprestimo import Emprestimo

def configure_all(app):
    configure_db()
    configure_routes(app)

def configure_routes(app):
    app.register_blueprint(home_route)
    app.register_blueprint(cliente_route, url_prefix='/clientes')
    app.register_blueprint(atendente_route, url_prefix='/atendentes')
    app.register_blueprint(editora_route, url_prefix='/editoras')
    app.register_blueprint(livro_route, url_prefix='/livros')
    app.register_blueprint(emprestimo_route, url_prefix='/emprestimos')


def configure_db():
    db.connect() # conexão com o banco de dados
    db.create_tables([Cliente, Atendente, Livro, Editora, Emprestimo]) # criação das tabelas do banco de dados (caso as tabelas já existirem ele irá carrega-las)