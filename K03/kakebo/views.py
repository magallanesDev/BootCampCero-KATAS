from kakebo import app
import sqlite3

@app.route('/')
def index():
    conexion = sqlite3.connect('movimientos.db')
    cur = conexion.cursor()

    cur.execute('SELECT * FROM movimientos;')  # las sentencias SQL se acaban en ;

    claves = cur.description

    filas = cur.fetchall()

    '''
    l = []  # creamos una lista vacía. Despúes será una lista de diccionarios
    for fila in filas:
        d = {}  # creamos un diccionario vacío
        for columna in fila:
            # usaremos enumarate o un índice
            # lo pasaremos a json la lista de diccionarios
    '''
        
    conexion.close()

    return 'Consulta realizada'
