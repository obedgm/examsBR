'''
Servidor del sistema.
Hace uso del microframework Flask para implementar la clase controladora de 
interfaz de usuario y el controlador de sesiones, asi como el servidor mismo.
'''

from flask import Flask, render_template, redirect, url_for, request, session
from backend.classes import User, Folder, Section, Question
import backend.classesUtils as cu
from backend.DBController import DBController
import backend.generatorUtils as gu

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']

    user = db.getUser(email)

    userId = user.getEmail()
    users[userId] = user
    session['userId'] = userId

    return redirect(url_for('main', 
        _scheme='https', _external=True), code = 307)

@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]

        userName = user.getName()

        email = user.getEmail()
        id = email.split("@")[0]
        
        db.loadFolders(user, id)

        folders = cu.formatFolders(user)
        foldersJSON = cu.formatFoldersJSON(user)

        return render_template('main.html', userName = userName, 
            folders = folders, foldersJSON = foldersJSON, 
            _scheme='https', _external=True)

    return render_template('home.html', notLogged = True)

@app.route('/newFolder', methods=['POST'])
def newFolder():
    if 'userId' in session:
        folderName = request.form["folderName"]
        folderId = folderName.strip()
        userId = session['userId']
        user = users[userId]

        db.addFolder(user, folderName, folderId)

        return redirect(url_for('editor', folderId = folderId, caller = "newFolder", 
            _scheme='https', _external=True), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/saveFolder', methods=['POST'])
def saveFolder():
    if 'userId' in session:
        folderId = request.form["0_0_folderId"]
        userId = session['userId']
        user = users[userId]
        cu.saveFolder(request.form, user, folderId)

        db.updateUserData(user, folderId)
        
        return redirect(url_for('editor', folderId = folderId, caller = "saveFolder", 
            _scheme='https', _external=True), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/openFolder', methods=['POST'])
def openFolder():
    if 'userId' in session:
        folderId = request.form["folderId"]
        
        return redirect(url_for('editor', folderId = folderId, caller = "openFolder", 
            _scheme='https', _external=True), code = 307)
   
    return render_template('home.html', notLogged = True)

@app.route('/delFolder', methods=['POST'])
def delFolder():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]
        folderId = request.form['folderId']
        
        db.deleteFolder(user, folderId)

        user.deleteFolder(folderId)

        return redirect(url_for('main', 
            _scheme='https', _external=True), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/editor/<folderId>/<caller>', methods=['POST'])
def editor(folderId, caller):
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]

        db.loadFolder(user, folderId)

        userName = user.getName()
        folderName = cu.getFolderName(user, folderId)

        contents = cu.getFormattedContents(user, folderId)

        sections = cu.formatSections(user, folderId)
        sectionsJSON = cu.formatSectionsJSON(user, folderId)

        return render_template('editor.html', userName = userName, caller = caller,
                                              folderName = folderName, folderId = folderId,
                                              sections = sections, sectionsJSON = sectionsJSON,
                                              contents = contents, 
                                              _scheme='https', _external=True)

    return render_template('home.html', notLogged = True)

@app.route('/displayFiles', methods=['GET', 'POST'])
def displayFiles():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]
        userName = user.getName()

        files = db.getUserFiles(user)

        if files:
            files = files.keys()
        else:
            files = {}

        return render_template('listFiles.html', files = files, userName = userName, 
            _scheme='https', _external=True)

    return render_template('home.html', notLogged = True)

@app.route('/generateExams', methods=['POST'])
def generateExams():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]
        folderId = request.form['folderId']

        error = gu.generateAlgebraics(request.form, user, folderId)
        contents = gu.formatForDynamicDisplay(request.form, user, folderId)

        folderName = cu.getFolderName(user, folderId)
        amount = request.form['amount']

        return render_template('gen.html', contents = contents, folderName = folderName, 
            amount = amount, error = error, 
            _scheme='https', _external=True)

    return render_template('home.html', notLogged = True)

@app.route('/viewFile', methods=['POST'])
def vieFile():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]
        fileName = request.form['fileName']

        content = db.getUserFiles(user)[fileName]['content']

        return render_template('view.html', content = content, 
            _scheme='https', _external=True)

    return render_template('home.html', notLogged = True)

@app.route('/saveFile', methods=['POST'])
def saveFile():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]
        fileName = request.form['fileName']
        fileContent = request.form['fileContent']

        db.saveFile(user, fileName, fileContent)

        return redirect(url_for('displayFiles', 
            _scheme='https', _external=True), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/deleteFile', methods=['POST'])
def deleteFile():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]
        fileName = request.form['fileName']

        db.deleteFile(user, fileName)

        return redirect(url_for('displayFiles', 
            _scheme='https', _external=True), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('userId', None)
    return render_template('home.html', 
        _scheme='https', _external=True)

if __name__ == '__main__':
    db = DBController()
    '''
    Llave de seguridad utilizada por la clase controladora de sesiones
    de Flask 
    '''
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    '''
    Diccionario que mantiene cargados los objetos de usuario
    LLave: correo del usuario
    Valor: instancia de usuario
    '''
    users = {}

    '''
    Clase controladora de iterfaz de usuario de Flask
    '''
    app.run()
