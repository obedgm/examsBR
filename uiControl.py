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
    '''
        Aqui espero que me mandes al usuario pelon sin folders
    '''
    # user = db.getUser(email)

    userId = user.getEmail()
    users[userId] = user
    session['userId'] = userId

    return redirect(url_for('main'), code = 307)

@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]

        userName = user.getName()
        '''
            Aqui espero que al usuario que te mande le insertes sus folders
            (Los folders sin secciones)
        '''
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

        '''
            Aqui espero que al usuario que te mande le insertes un folder 
            con el nombre y ID que te mando 
            (insertar tanto en la bd como el objeto)
        '''
        db.addFolder(user, folderName, folderId)

        return redirect(url_for('editor', folderId = folderId, caller = "newFolder"), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/saveFolder', methods=['POST'])
def saveFolder():
    if 'userId' in session:
        folderId = request.form["0_0_folderId"]
        userId = session['userId']
        user = users[userId]
        cu.saveFolder(request.form, user, folderId)

        '''
            Aqui espero te mando un usuario que tiene folder, secciones y preguntas
            Este esta bien implementado
        '''
        db.updateUserData(user)
        
        return redirect(url_for('editor', folderId = folderId, caller = "saveFolder"), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/openFolder', methods=['POST'])
def openFolder():
    if 'userId' in session:
        folderId = request.form["folderId"]
        
        return redirect(url_for('editor', folderId = folderId, caller = "openFolder"), code = 307)
   
    return render_template('home.html', notLogged = True)

@app.route('/delFolder', methods=['POST'])
def delFolder():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]
        folderId = request.form['folderId']
        
        '''
        Aqui te mando un usuario y el id del folder a borrar (solo de la bd)
        '''
        # db.deleteFolder(user, folderId)

        user.deleteFolder(folderId)

        return redirect(url_for('main'), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/editor/<folderId>/<caller>', methods=['POST'])
def editor(folderId, caller):
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]

        '''
        Aqui te mando un usuario y el id del folder, ocupo que agregas al 
        objeto usuario el objeto folder con secciones y preguntas
        '''
        db.loadQuestions(user, folderId)

        userName = user.getName()
        folderName = cu.getFolderName(user, folderId)

        contents = cu.getFormattedContents(user, folderId)

        sections = cu.formatSections(user, folderId)
        sectionsJSON = cu.formatSectionsJSON(user, folderId)

        return render_template('editor.html', userName = userName, caller = caller,
                                              folderName = folderName, folderId = folderId,
                                              sections = sections, sectionsJSON = sectionsJSON,
                                              contents = contents)

    return render_template('home.html', notLogged = True)

@app.route('/displayFiles', methods=['GET', 'POST'])
def displayFiles():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]

        '''
        Aqui espero que me mandes un diccionario de nombres de folders a htmls
        yo saco las llaves para desplegar los nombres en la UI
        '''
        files = db.getUserFiles(user).keys()

        return render_template('listFiles.html', files = files)

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

        return render_template('gen.html', contents = contents, folderName = folderName, amount = amount)

    return render_template('home.html', notLogged = True)

@app.route('/viewFile', methods=['POST'])
def vieFile():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]
        fileName = request.form['fileName']

        '''
        Aqui espero que me mandes un diccionario de nombres de folders a htmls
        yo saco el html usando el folder
        '''
        content = db.getUserFiles(user)[fileName]

        return render_template('view.html', content = content)

    return render_template('home.html', notLogged = True)

@app.route('/saveFile', methods=['POST'])
def saveFile():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]
        fileName = request.form['fileName']
        fileContent = request.form['fileContent']

        '''
        te mando un usuario y el nombre del archivo y el html para
        guardar en la bd
        '''
        # db.saveFile(user, fileName, fileContent)

        return redirect(url_for('displayFiles'), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/deleteFile', methods=['POST'])
def deleteFile():
    if 'userId' in session:
        userId = session['userId']
        user = users[userId]
        fileName = request.form['fileName']

        '''
        te mando el usuario y el nombre del archivo para que lo 
        borres de la bd
        '''
        # db.deleteFile(user, fileName)

        return redirect(url_for('displayFiles'), code = 307)

    return render_template('home.html', notLogged = True)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('userId', None)
    return render_template('home.html')

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
    app.run(debug = True)
