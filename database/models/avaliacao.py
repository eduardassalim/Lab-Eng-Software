from peewee import Model, IntegerField, DateTimeField, ForeignKeyField
from database.models.livro import Livro
from database.models.emprestimo import Emprestimo
from database.database import db
import datetime

class Avaliacao(Model):
    livro = ForeignKeyField(Livro, backref='avaliacoes')
    emprestimo = ForeignKeyField(Emprestimo, backref='avaliacoes', unique=True)  # O empréstimo que realizou a avaliação
    nota = IntegerField()
    data_registro = DateTimeField(default = datetime.datetime.now)
    
    class Meta:
        database = db