from flask import Flask, render_template, redirect, url_for, request
from code.classes.py import User
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/main', methods=['POST'])
def main():
    u = request.form["user"];
    return render_template('main.html', user = u)

@app.route('/newEval', methods=['POST'])
def newEval():
    n = request.form['name']
    u = request.form["user"]
    # PENDIENTE CREAR OBJETO EVAL en BD
    return redirect(url_for('openEval', name = n, user = u), code = 307)

@app.route('/openEval/<name>/<user>', methods=['POST'])
def openEval(name, user):
    # PENDIENTE traer la evaluacion y preguntas de BD
    return render_template('editor.html', evalName = name, user = user)

@app.route('/submitEval', methods=['POST'])
def submitEval():
    return null;

if __name__ == '__main__':
    app.run(debug = True)