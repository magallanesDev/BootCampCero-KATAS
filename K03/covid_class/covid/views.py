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


@app.route('/casos/<int:year>/<int:mes>/<int:dia>')
def casos(year, mes, dia):
    fichero = open('data/casos_diagnostico_provincia.csv', 'r')
    dictreader = csv.DictReader(fichero)
    sumaCasos = 0
    for registro in dictreader:
        if registro['fecha'] == str(year) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2):
            sumaCasos += int(registro['num_casos'])
    fichero.close()
    return str(sumaCasos)
    
    
#  @app.route('/casos/<int:year>' defaults={'mes:None', dia:None})
#  @app.route('/casos/<int:year>/<int:mes>', defaults={'dia':None})