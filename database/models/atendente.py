from peewee import Model, CharField, DateTimeField
from database.database import db
import datetime

class Atendente(Model):
    nome = CharField()
    email = CharField()
    cargo = CharField()
    data_registro = DateTimeField(default = datetime.datetime.now)
    
    class Meta:
        database = db