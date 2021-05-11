from flask import Flask  # importamos la clase Flask

app = Flask(__name__)  # crea una instancia de la clase Flask

@app.route('/')  # decorador
def index():     # función
    return 'Hola, mundo'

@app.route('/adios')  # decorador
def bye():            # función
    return 'Hasta luego, cocodrilo'
