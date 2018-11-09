from flask import Flask, render_template, redirect, url_for, request, session
from backend.classes import User, Evaluation, Question
import backend.classesUtils as cu
from backend.DBController import DBController

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    userName = request.form["userName"]
    userId = str(request.form["userId"])
    email = request.form["email"]

    session['userId'] = userId
    user = db.getOrCreateUser(userName, userId, email)
    users[userId] = user

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
        evalId = request.form["0_evalId"]
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
        questions = cu.getFormattedQuestions(user, evalId)

        return render_template('editor.html', userName = userName,
                                              evalName = evalName, evalId = evalId,
                                              questions = questions, caller = caller)

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
