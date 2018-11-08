from flask import Flask, render_template, redirect, url_for, request, session
from backend.classes import User, Folder, Section, Question
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
        db.loadFolders(user)

        folders = cu.formatFolders(user)
        foldersJSON = cu.formatFoldersJSON(user)

        return render_template('main.html', userName = userName, 
            folders = folders, foldersJSON = foldersJSON)

    return render_template('home.html', notLogged = True)

@app.route('/newFolder', methods=['POST'])
def newFolder():
    if 'userId' in session:
        folderName = request.form["folderName"]
        folderId = folderName.strip()
        userId = session['userId']
        user = users[userId]

        db.addFolder(user, folderName, folderId)

        return redirect(url_for('editor', folderId = folderId, caller = "newFolder"), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/saveFolder', methods=['POST'])
def saveFolder():
    if 'userId' in session:
        print(str(request.form))
        folderId = request.form["0_0_folderId"]
        userId = session['userId']
        user = users[userId]
        cu.saveFolder(request.form, user, folderId)
        db.updateUserData(user)
        
        return redirect(url_for('editor', folderId = folderId, caller = "saveFolder"), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/openFolder', methods=['POST'])
def openFolder():
    if 'userId' in session:
        folderId = request.form["folderId"]
        
        return redirect(url_for('editor', folderId = folderId, caller = "openFolder"), code = 307)
   
    return render_template('home.html', notLogged = True)

@app.route('/editor/<folderId>/<caller>', methods=['POST'])
def editor(folderId, caller):
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]

        db.loadQuestions(user, folderId)

        userName = user.getName()
        folderName = cu.getFolderName(user, folderId)

        contents = cu.getFormattedContents(user, folderId)

        #sections = cu.formatSections(user, folderId)
        #sections = cu.formatSectionsJSON(user, folderId)

        return render_template('editor.html', userName = userName,
                                              folderName = folderName, folderId = folderId,
                                              contents = contents, caller = caller)

    return render_template('home.html', notLogged = True)

@app.route('/delFolder', methods=['POST'])
def delFolder():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]
        folderId = request.form['folderId']
        '''
        Enviar a la BD y borrar
        '''
        user.deleteFolder(folderId)

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
