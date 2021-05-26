from kakebo import app
from flask import jsonify, render_template, request, redirect, url_for
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
    formulario = MovimientosForm()
    if request.method == 'GET':
        return render_template('alta.html', form = formulario)
    else:  # será un POST
        if formulario.validate():  # insertar el movimiento en la base de datos
            conexion = sqlite3.connect('movimientos.db')
            cur = conexion.cursor()

            query = """ INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad)
                        VALUES (?, ?, ?, ?, ?) """
            try:
                cur.execute(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
                                    formulario.esGasto.data, formulario.cantidad.data])
            except sqlite3.Error as el_error:
                print("ERROR EN SQL", el_error)
                return render_template('alta.html', form = formulario)
            
            conexion.commit()  # fijamos el movimiento en la base de datos
            conexion.close()

            return redirect(url_for('index'))  # redirect a la ruta / a través de la función index
        else:
            return render_template('alta.html', form = formulario)
