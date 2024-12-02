from peewee import Model, CharField, DateTimeField, ForeignKeyField, BooleanField
from database.models.editora import Editora
from database.database import db
import datetime

class Livro(Model):
    titulo = CharField()
    autor = CharField()
    ISBN = CharField()
    editora = ForeignKeyField(Editora, backref='livro')
    data_lancamento = DateTimeField()
    disponivel = BooleanField(default=True)
    data_registro = DateTimeField(default = datetime.datetime.now)
    
    class Meta:
        database = db