from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/main', methods=['POST'])
def main():
    return render_template('main.html')

@app.route('/newEval', methods=['POST'])
def newEval():
    n = request.form['name']
    # PENDIENTE CREAR OBJETO EVAL en BD
    return redirect(url_for('openEval', name = n))

@app.route('/openEval/<name>', methods=['GET', 'POST'])
def openEval(name):
    # PENDIENTE traer la evaluacion y preguntas de BD
    return render_template('editor.html', evalName = name)

if __name__ == '__main__':
    app.run(debug = True)