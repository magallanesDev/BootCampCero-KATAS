import sqlite3
from flask.json import jsonify
from kakebo import app
from kakebo.dataaccess import DBmanager
from flask import jsonify
import sqlite3


dbManager = DBmanager(app.config.get('DATABASE'))

@app.route('/api/v1/movimientos')
def movimientos():
    query = "SELECT * FROM movimientos ORDER BY fecha;"
    
    try:
        lista = dbManager.consultaMuchasSQL(query)
        return jsonify({'status': 'success', 'movimientos': lista})
    except sqlite3.Error as e:
        return jsonify({'status': 'fail', 'mensaje': str(e)})