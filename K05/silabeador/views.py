from silabeador import app
from silabeador.tools import pilengua
from flask import jsonify
import requests

@app.route("/pilengua/<frase>")
def enlenguapi(frase):
    respuesta = pilengua(frase)
    d = { 'original' : frase,
        'pilengua' : respuesta }
    return jsonify(d)


@app.route("/pelicula/<palabra>")
def pelicula(palabra):
    url = "http://www.omdbapi.com/?s={}&apikey=2bf0cc92"

    resultado = requests.get(url.format(palabra))
    if resultado.status_code == 200:
        peliculas = resultado.json()
        if peliculas['Response'] == "False":
            return jsonify({'status': "Error", "msg": "No se han encontrado resultados"})

        return jsonify({"Películas": peliculas["Search"], 'status': "Success"})