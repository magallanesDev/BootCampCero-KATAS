from flask import Flask

app = Flask(__name__)

from covid import views  # importamos las rutas