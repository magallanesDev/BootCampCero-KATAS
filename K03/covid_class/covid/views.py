from covid import app

@app.route('/')
def index():
    return "Flask está funcionando desde views!!!"