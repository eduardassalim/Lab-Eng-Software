from peewee import Model, CharField, DateTimeField
from database.database import db
import datetime

class Livro(Model):
    titulo = CharField()
    autor = CharField()
    ISBN = CharField()
    data_lancamento = DateTimeField()
    data_registro = DateTimeField(default = datetime.datetime.now)
    
    class Meta:
        database = db