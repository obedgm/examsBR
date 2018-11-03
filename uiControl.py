from flask import Flask, render_template, redirect, url_for, request
import json
#Ejemplo de como importar paquetes
#from backend.classes import User

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/main', methods=['POST'])
def main():
    userName = request.form["userName"]
    userId = request.form["userId"]
    email = request.form["email"]
    '''
    Envio datos del usuario al controlador de sesiones.
    Si existe el usuario en la base de datos no hago nada.
    Si no existe lo agrego.
    '''
    return render_template('main.html', userName = userName, userId = userId)

@app.route('/newEval', methods=['POST'])
def newEval():
    userId = request.form["userId"]
    evalName = request.form["evalName"]
    evalId = evalName.strip()
    '''
    Envio datos al controlador
    Creo la evaluacion ligada al usuario
    Si ya existe una evaluacion pues se va a abrir esa evaluacion
        y agregamos un mensaje de que ya existia (o si nos queda 
        tiempo hacemos algo mas fancy)
    '''
    return redirect(url_for('editor', userId = userId, evalId = evalId, caller = "newEval"), code = 307)

@app.route('/saveEval', methods=['POST'])
def saveEval():
    userId = request.form["userId"]
    evalName = request.form["evalId"]
    '''
    Envio al backend request.form para guardarlo en la BD
    '''
    return redirect(url_for('editor', userId = userId, evalId = evalId, caller = "saveEval"), code = 307)

@app.route('/editor/<userId>/<evalId>/<caller>', methods=['POST'])
def editor(userId, evalId, caller):
    '''
    Este metodo sera llamado por newEval y openEval, que podria abrir una
        evalaucion nueva o una que ya existia.
    '''
    questions = []
    questions.append({
        'statement': 'pregunta',
        'correct': 'correcta',
        'distractor1': 'distractor1',
        'distractor2': 'distractor2',
        'distractor3': 'distractor3'
    })
    questions.append({
        'algebraic': 'true',
        'statement': 'pregunta',
        'formula': 'formula'
    })

    userName = 'usuario'
    evalName = 'evaluacion'

    return render_template('editor.html', userName = userName, userId = userId,
                                          evalName = evalName, evalId = evalId,
                                          questions = questions, caller = caller)

@app.route('/submitEval', methods=['POST'])
def submitEval():
    return null;

if __name__ == '__main__':
    app.run(debug = True)