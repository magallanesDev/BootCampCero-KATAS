from kakebo import app
from flask import jsonify, render_template, request
from kakebo.forms import MovimientosForm
import sqlite3

@app.route('/')
def index():
    conexion = sqlite3.connect('movimientos.db')
    cur = conexion.cursor()

    cur.execute('SELECT * FROM movimientos;')  # las sentencias SQL se acaban en ;

    claves = cur.description
    filas = cur.fetchall()

    movimientos = []  # creamos una lista vacía. Despúes será una lista de diccionarios
    saldo = 0
    for fila in filas:
        d ={}  # creamos un diccionario vacío
        for tuplaClave, valor in zip(claves, fila):
            d[tuplaClave[0]] = valor
        if d['esGasto'] == 0:
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo
        movimientos.append(d)  

    conexion.close()

    # return jsonify(movimientos)
    return render_template('movimientos.html', datos = movimientos)


@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    form = MovimientosForm()
    return render_template('alta.html', form = form)

