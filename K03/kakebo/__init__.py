from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')  # nombre del fichero de configuración sin la extensión (config.py)

import kakebo.views
# equivalente a: from kakebo import views

