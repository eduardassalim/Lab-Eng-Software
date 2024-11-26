from peewee import Model, DateTimeField, ForeignKeyField
from database.database import db
from database.models.cliente import Cliente
from database.models.livro import Livro
import datetime

class Emprestimo(Model):
    cliente = ForeignKeyField(Cliente, backref='emprestimo')
    livro = ForeignKeyField(Livro, backref='emprestimo')
    data_emprestimo = DateTimeField()
    data_devolucao = DateTimeField()
    data_registro = DateTimeField(default = datetime.datetime.now)
    
    class Meta:
        database = db