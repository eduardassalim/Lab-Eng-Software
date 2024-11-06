from peewee import Model, CharField, DateTimeField
from database.database import db
import datetime

class Editora(Model):
    nome = CharField()
    endereco = CharField()
    telefone = CharField()
    CNPJ = CharField()
    data_registro = DateTimeField(default = datetime.datetime.now)
    
    class Meta:
        database = db