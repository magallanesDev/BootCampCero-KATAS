from flask import render_template, request
from covid import app
import csv
import json

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
    
    
@app.route('/incidenciadiaria', methods = ['GET', 'POST'])
def incidencia():
    if request.method == 'GET':
        return render_template('alta.html')
    
    return "Se ha hecho un post"
    