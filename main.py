from flask import Flask # importação do método Flask
from configuration import configure_all

app = Flask(__name__) # inicialização padrão do aplicativo Flask

configure_all(app)

# verifica se o programa está sendo rodado no main e roda a aplicação Flask
if (__name__ == '__main__'):
    app.run(debug=True)