'''
Clase controladora de la base de datos.
Provee de metodos para acceder y modificar la base de datos.
'''

from classes import User, Folder, Section, Question
import classesUtils as cu
import pyrebase

class DBController:

    def __init__(self):
        self.__firebase = pyrebase.initialize_app(config)
        self.__db = firebase.database()

    def getUser(self, email):
        db = self.__db

        id = email.split("@")[0]

        name = db.child(id).child("name").get().val()

        if(name):
            user = User(name, email)
            self.loadFolders(user, id)            

        return user

    def loadFolders(self, user, id):
        db = self.__db

        folderDict = db.child(id).child('Folder').get().val()

        if folderDict:
            pregunta = Question("", False)
            for folder in reversed(folderDict):
                userFolder = Folder(folder, folder)
                user.addFolder(userFolder)

        return user

        user.addFolder(e1)

    def loadFolder(self, user, folderId):
        db = self.__db

        folder = Folder(folderId, folderId)

        id = user.getEmail().split("@")[0]
        print(id)
        print(folderId)
        folderDict = db.child(id).child('Folder').child(folderId).get().val()
        print(folderDict)

        pregunta = Question("", False)
        for item in reversed(folderDict):
            section = Section(item)
            print(item)
            for a in folderDict[item]:
                for val in a:
                    if val == 'pregunta':
                        pregunta = Question(a[val], False)
                    elif val == 'distractor1':
                        pregunta.addDistractor(a[val])
                    elif val == 'distractor2':
                        pregunta.addDistractor(a[val])
                    elif val == 'distractor3':
                        pregunta.addDistractor(a[val])
                    elif val == 'correcta':
                        pregunta.setCorrect(a[val])
                    elif val == 'algebra':
                        b = a[val]
                    elif val == 'formula':
                        c = a[val]
                if not pregunta.getStatement():
                    preguntaAlg = Question(b, True)
                    preguntaAlg.setFormula(c)
                    section.addQuestion(preguntaAlg)
                else:
                    section.addQuestion(pregunta)

            folder.addSection(section)

        user.addFolder(folder)

    def updateUserData(self, user, folderId):
        db = self.__db

        id = user.getEmail().split("@")[0]
        folder = user.getFolder(folderId)
        sections = folder.getSections()

        db.child(id).child("Folder").child(folderId).remove()

        for section in sections:
            questions = section.getQuestions()
            count = 0

            for question in questions:
                if(question.getAlgebraic()):
                    data = {
                        id + "/" + "Folder/" + folder.getId() + "/" + section.getName() + "/" + str(count) + "/": {
                            "algebra": question.getStatement(),
                            "formula": question.getFormula()
                        }
                    }
                    db.update(data)
                else:
                    data = {
                        id + "/" + "Folder/" + folder.getId() + "/" + section.getName() + "/" + str(count) + "/": {
                            "pregunta": question.getStatement(),
                            "distractor1": question.getDistractors()[0],
                            "distractor2": question.getDistractors()[1],
                            "distractor3": question.getDistractors()[2],
                            "correcta": question.getCorrect()
                        }
                    }
                    db.update(data)
                count += 1

        db.child(id).child('Folder').child(folderId).child("placeholder").remove()

    def addFolder(self, user, folderName, folderId):
        db = self.__db

        id = user.getEmail().split("@")[0]
        print("this is the id")
        print(id)

        data = {
            id + "/" + "Folder/" + folderId + "/" +  "placeholder/0/": {
                "pregunta": "placeholder",
                "distractor1": "placeholder",
                "distractor2": "placeholder",
                "distractor3": "placeholder",
                "correcta": "placeholder"
            }
        }
        db.update(data)

    def saveFile(self, user, fileName, fileContent):
        db = self.__db

        id = user.getEmail().split("@")[0]
        data = {
            id + "/" + "Files/" + fileName + "/": {
                "content": fileContent
            }
        }
        db.update(data)

    def getUserFiles(self, user):
        db = self.__db

        id = user.getEmail().split("@")[0]

        fileDict = db.child(id).child('Files').get().val()

        return fileDict

    def deleteFile(self, user, fileName):
        db = self.__db

        id = user.getEmail().split("@")[0]

        db.child(id).child('Files').child(fileName).remove()

    def deleteFolder(self, user, folderId):
        db = self.__db

        id = user.getEmail().split("@")[0]

        db.child(id).child('Folder').child(folderId).remove()

config = {
  "apiKey": "AIzaSyCMs1O70z1q6qIArA36dBX1iuipaNStOYg",
  "authDomain": "examsbr-2a061.firebaseapp.com",
  "databaseURL": "https://examsbr-2a061.firebaseio.com",
  "storageBucket": "",
}

firebase = pyrebase.initialize_app(config)

