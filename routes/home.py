from flask import Blueprint, render_template

home_route = Blueprint('home', __name__)

# rota raiz
@home_route.route('/')
def home():
    return render_template('index.html')