from kakebo import app
from flask import jsonify, render_template, request, redirect, url_for, flash
from kakebo.forms import MovimientosForm, FiltraMovimientosForm
from datetime import date
import sqlite3


def consultaSQL(query, parametros=[]):
    # Abrimos la conexión
    conexion = sqlite3.connect('movimientos.db')
    cur = conexion.cursor()

    # Ejecutamos la consulta
    cur.execute(query, parametros)

    # Obtenemos los datos de la consulta
    claves = cur.description
    filas = cur.fetchall()

    # Procesar los datos para devolver una lista de dicionarios. Um diccionario por fila
    resultado = []  # creamos una lista vacía. Despúes será una lista de diccionarios
    for fila in filas:
        d ={}  # creamos un diccionario vacío
        for tuplaClave, valor in zip(claves, fila):
            d[tuplaClave[0]] = valor
        
        resultado.append(d)

    conexion.close()
    return resultado



def modificaTablaSQL(query, parametros=[]):
    conexion = sqlite3.connect('movimientos.db')
    cur = conexion.cursor()

    cur.execute(query, parametros)

    conexion.commit()
    conexion.close()
    


@app.route('/', methods=['GET', 'POST'])
def index():
    filtraForm = FiltraMovimientosForm()  # Instanciamos el formulario
    query = "SELECT * FROM movimientos WHERE 1=1" # El WHERE 1=1 siempre se cumple, aquí no haría nada,
                                                      # es una pequeña trampa para añadir otra condición después. 
    parametros = []

    if request.method == 'POST':
        if filtraForm.validate():  
            if filtraForm.fechaDesde.data != None:
                query += " AND fecha >= ?"
                parametros.append(filtraForm.fechaDesde.data)
            if filtraForm.fechaHasta.data != None:
                query += " AND fecha <= ?"
                parametros.append(filtraForm.fechaHasta.data)
            if filtraForm.texto.data != '':
                query += ' AND concepto LIKE ?'
                parametros.append("%{}%".format(filtraForm.texto.data))

    query += " ORDER BY fecha"
    movimientos = consultaSQL(query, parametros)

    saldo = 0
    for d in movimientos:
        if d['esGasto'] == 0:
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo 

    return render_template('movimientos.html', datos = movimientos, formulario = filtraForm)



@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    formulario = MovimientosForm()
    if request.method == 'GET':
        return render_template('alta.html', form = formulario)
    else:  # será un POST
        if formulario.validate():  # insertar el movimiento en la base de datos

            query = """ INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad)
                        VALUES (?, ?, ?, ?, ?) """
            try:
                modificaTablaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
                                    formulario.esGasto.data, formulario.cantidad.data])
            except sqlite3.Error as el_error:
                print("ERROR EN SQL", el_error)
                flash('Se ha producido un error en la base de datos. Pruebe en unos minutos')
                return render_template('alta.html', form = formulario)

            return redirect(url_for('index'))  # redirect a la ruta / a través de la función index
        else:
            return render_template('alta.html', form = formulario)



@app.route('/borrar/<int:id>', methods=['GET', 'POST'])
def borrar(id):
    if request.method =='GET':
        filas = consultaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if len(filas)  == 0:
            flash('El registro no existe')    
            return render_template('borrar.html')

        return render_template('borrar.html', movimiento = filas[0])
    else:
        try:
            modificaTablaSQL("DELETE FROM movimientos WHERE id = ?;", [id])
        except sqlite3.Error as e:
            flash('Se ha producido un error de base de datos, vuelva a intentarlo', 'error')
            return redirect(url_for('index'))

        flash('Borrado realizado con éxito', 'aviso')
        return redirect(url_for('index')) 



@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    if request.method =='GET':
        filas = consultaSQL("SELECT * FROM movimientos WHERE id = ?", [id])
        if len(filas)  == 0:
            flash('El registro no existe', "error")    
            return render_template('modificar.html')
        registro = filas[0]
        registro['fecha'] = date.fromisoformat(registro['fecha'])
    
        formulario = MovimientosForm(data = registro)

        return render_template('modificar.html', form = formulario)
    else:
        formulario = MovimientosForm()
        if formulario.validate():  # validamos el formulario

            query = "UPDATE movimientos SET fecha=?, concepto=?, categoria=?, esGasto=?, cantidad=? WHERE id=?;"
            try:
                modificaTablaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
                                    formulario.esGasto.data, formulario.cantidad.data, id])
        
            except sqlite3.Error as e:
                print("Error en update:", e)
                flash('Se ha producido un error de base de datos. Contacte con administrador', 'error')
                return render_template('modificar.html', form = formulario)

            flash('Modificación realizada con éxito', 'aviso')
            return redirect(url_for('index'))
            
        else:
            return render_template('modificar.html', form = formulario)