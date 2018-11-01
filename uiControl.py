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
    print("****\n", request.form)
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
    userName = request.form["userName"]
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
    return redirect(url_for('editor', userName = userName, userId = userId, evalName = evalName, evalId = evalId), code = 307)

@app.route('/editor/<userName>/<userId>/<evalName>/<evalId>', methods=['POST'])
def editor(userName, userId, evalName, evalId):
    '''
    Este metodo sera llamado por newEval y openEval, que podria abrir una
        evalaucion nueva o una que ya existia.
    '''
    evaluation = {}
    evaluation['questions'] = []
    evaluation['questions'].append({
        'algebraic': 'false',
        'statement': 'pregunta',
        'correct': 'correcta',
        'distractors' : {
            'distractor1',
            'distractor2',
            'distractor3'
        }
    })
    evaluation['questions'].append({
        'algebraic': 'true',
        'statement': 'pregunta',
        'formula': 'formula'
    })

    return render_template('editor.html', userName = userName, userId = userId,
                                          evalName = evalName, evalId = evalId,
                                          evaluation = evaluation)

@app.route('/submitEval', methods=['POST'])
def submitEval():
    return null;

if __name__ == '__main__':
    app.run(debug = True)