from silabeador import app

@app.route("/pilengua/<frase>")
def pilengua(frase):
    return "Has escrito " + frase