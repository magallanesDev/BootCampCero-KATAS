from flask import render_template, request
from covid import app
import csv
import json
from datetime import date


@app.route('/provincias')
def provincias():
    fichero = open('data/provincias.csv', 'r')
    csvreader = csv.reader(fichero, delimiter=',')  # guarda en forma de lista cada registro

    lista = []
    for registro in csvreader:
        d = {'codigo': registro[0], 'valor': registro[1]}
        lista.append(d)  # será una lista de diccionarios

    fichero.close()
    print(lista)
    return json.dumps(lista)  # transformamos la lista a formato json


@app.route('/provincia/<codigoProvincia>')
def laprovincia(codigoProvincia):
    fichero = open('data/provincias.csv', 'r')
    dictreader = csv.DictReader(fichero, fieldnames=['codigo', 'provincia'])
    for registro in dictreader:
        if registro['codigo'] == codigoProvincia:
            fichero.close()
            return registro['provincia']
    
    fichero.close()
    return "La provincia no existe"


@app.route('/casos/<int:year>', defaults={'mes':None, 'dia':None})
@app.route('/casos/<int:year>/<int:mes>', defaults={'dia':None})
@app.route('/casos/<int:year>/<int:mes>/<int:dia>')
def casos(year, mes, dia):
    if not mes:
        fecha = '{:04d}'.format(year)
    elif not dia:
        fecha = '{:04d}-{:02d}'.format(year, mes)
    else:
        fecha = '{:04d}-{:02d}-{:02d}'.format(year, mes, dia)

    fichero = open('data/casos_diagnostico_provincia.csv', 'r')
    dictreader = csv.DictReader(fichero)
    
    res ={ 
    'num_casos': 0,
    'num_casos_prueba_pcr': 0,
    'num_casos_prueba_test_ac': 0,
    'num_casos_prueba_ag': 0,
    'num_casos_prueba_elisa': 0,
    'num_casos_prueba_desconocida': 0
    }
    for registro in dictreader:
        if fecha in registro['fecha']:
            for clave in res:
                res[clave] += int(registro[clave])
        
        elif registro['fecha'] > fecha:
            break
    
    fichero.close()
    return json.dumps(res)
    
    
@app.route("/incidenciasdiarias", methods = ['GET', 'POST'])
def incidencia():
    formulario = {
        'provincia': '',
        'fecha': str(date.today()),
        'num_casos_prueba_pcr': 0,
        'num_casos_prueba_test_ac': 0, 
        'num_casos_prueba_ag': 0,
        'num_casos_prueba_elisa': 0,
        'num_casos_prueba_desconocida': 0
    }
    fichero = open('data/provincias.csv', 'r')
    csvreader = csv.reader(fichero, delimiter=",")
    next(csvreader)
    lista = []
    for registro in csvreader:
        d = {'codigo': registro[0], 'descripcion': registro[1]}
        lista.append(d)
    fichero.close()
    if request.method == 'GET':
        return render_template("alta.html", datos=formulario, 
                               provincias=lista, error="")
    for clave in formulario:
        formulario[clave] = request.form[clave]
    #validar que num_casos en general es no negativo
    num_pcr = request.form['num_casos_prueba_pcr']
    try:
        num_pcr = int(num_pcr)
        if num_pcr < 0:
            raise ValueError('Debe ser no negativo')
    except ValueError:
        return render_template("alta.html", datos=formulario, error = "PCR no puede ser negativa")
    return 'Ha hecho un post'
    