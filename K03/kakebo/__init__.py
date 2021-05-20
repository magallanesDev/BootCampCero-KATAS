from flask import Flask

app = Flask(__name__)

import kakebo.views
# equivalente a: from kakebo import views

