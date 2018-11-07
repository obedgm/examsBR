from flask import Flask, render_template, redirect, url_for, request, session
from backend.classes import User, Evaluation, Section, Question
import backend.classesUtils as cu
from backend.DBController import DBController

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    # Trae usuario de la base de datos

    # mock data
    user = User("Juan", "1", "juan@hola.com")
    # end mock data

    userId = user.getId()
    users[userId] = user
    session['userId'] = userId

    return redirect(url_for('main'), code = 307)

@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]

        userName = user.getName()
        db.loadEvaluations(user)

        evaluations = cu.formatEvaluations(user)
        evaluationsJSON = cu.formatEvaluationsJSON(user)

        return render_template('main.html', userName = userName, 
            evaluations = evaluations, evaluationsJSON = evaluationsJSON)

    return render_template('home.html', notLogged = True)

@app.route('/newEval', methods=['POST'])
def newEval():
    if 'userId' in session:
        evalName = request.form["evalName"]
        evalId = evalName.strip()
        userId = session['userId']
        user = users[userId]

        db.addEvaluation(user, evalName, evalId)

        return redirect(url_for('editor', evalId = evalId, caller = "newEval"), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/saveEval', methods=['POST'])
def saveEval():
    if 'userId' in session:
        print(str(request.form))
        evalId = request.form["0_0_evalId"]
        userId = session['userId']
        user = users[userId]
        cu.saveEvaluation(request.form, user, evalId)
        db.updateUserData(user)
        
        return redirect(url_for('editor', evalId = evalId, caller = "saveEval"), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/openEval', methods=['POST'])
def openEval():
    if 'userId' in session:
        evalId = request.form["evalId"]
        
        return redirect(url_for('editor', evalId = evalId, caller = "openEval"), code = 307)
   
    return render_template('home.html', notLogged = True)

@app.route('/editor/<evalId>/<caller>', methods=['POST'])
def editor(evalId, caller):
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]

        db.loadQuestions(user, evalId)

        userName = user.getName()
        evalName = cu.getEvalName(user, evalId)

        contents = cu.getFormattedContents(user, evalId)

        return render_template('editor.html', userName = userName,
                                              evalName = evalName, evalId = evalId,
                                              contents = contents, caller = caller)

    return render_template('home.html', notLogged = True)

@app.route('/delEval', methods=['POST'])
def delEval():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]
        evalId = request.form['evalId']
        '''
        Enviar a la BD y borrar
        '''
        user.deleteEvaluation(evalId)

        return redirect(url_for('main'), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('userId', None)
    return render_template('home.html')

if __name__ == '__main__':
    db = DBController()
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    users = {}
    app.run(debug = True)
