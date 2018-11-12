from classes import User, Folder, Section, Question
import classesUtils as cu
import pyrebase

class DBController:

    def getOrCreateUser(self, userName, userId, email):
        # Busca en la BD el usuario y si no lo crea
        # Toma el output de la BD y en otra funcion
        #   lo restructura a clases

        user = User(userName, userId, email)

        # Agrega usuario a la bd

        return user

    def loadFolders(self, user):
        user.clearFolders()
        # Trae desde la base de datos todas las 
        #   carpetas del usuario y las agrega
        #   al usuario

        # mock data
        e1 = Folder("Historia 1", "Historia1")
        # end mock data

        user.addFolder(e1)

    def addFolder(self, user, folderName, folderId):
        folder = Folder(folderName, folderId)
        user.addFolder(folder)
        # Guarda la carpeta en la BD

    def loadFolder(self, user, folderId):
        # Trae la carpeta de la bd y se la pone
        #   al usuario

        # mock data
        folder = Folder("nombre", folderId)
        # end mock data

        user.addFolder(folder)

    def loadQuestions(self, user, folderId):
        user.clearFolders()
        self.loadFolder(user, folderId)
        # Trae las preguntas desde la bd y se las
        #   pone a la carpeta y al usuario
        
        e1 = user.getFolder(folderId)

        # mock data
        q1 = Question("Que paso?", False)
        q1.setCorrect("Correcto")
        q1.addDistractor("Distractor1")
        q1.addDistractor("Distractor2")
        q1.addDistractor("Distractor3")

        q2 = Question("Que paso pt2?", True)
        q2.setFormula("X + Y")

        s1 = Section("Porfiriato")
        s1.addQuestion(q1)
        s1.addQuestion(q2)
        # end mock data

        e1.addSection(s1)

    def updateUserData(self, user):
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()

        id = user.getName().split("@")[0]
        folder = user.getFolders()[0] #placeholder
        sections = folder.getSections()

        db.child(id).child('Folder').child(folder.getName()).remove()

        for section in sections:
            questions = section.getQuestions()
            count = 0

            for question in questions:
                data = {
                    id + "/" + "Folder/" + folder.getName() + "/" + section.getName() + "/" + str(count) + "/": {
                        "pregunta": question.getStatement(),
                        "distractor1": question.getDistractors()[0],
                        "distractor2": question.getDistractors()[1],
                        "distractor3": question.getDistractors()[2],
                        "correcta": question.getCorrect()
                    }
                }
                db.update(data)
                count += 1

        return 0


    def getUserData(self, user, folderName, folderId):
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()

        folder = Folder(folderName, folderId)

        folderDict = db.child(user.getId()).child('Folder').child(folderName).val().get()

        folderDict = db.child(id).child('Folder').child(folder.getName()).get().val()

        folder = Folder(folderName, folderId)

        pregunta = Question("", False)
        for item in folderDict:
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

                section.addQuestion(pregunta)

            folder.addSection(section)

        return folder



#conectar a la BD
config = {
  "apiKey": "AIzaSyCMs1O70z1q6qIArA36dBX1iuipaNStOYg",
  "authDomain": "examsbr-2a061.firebaseapp.com",
  "databaseURL": "https://examsbr-2a061.firebaseio.com",
  "storageBucket": "",
}

firebase = pyrebase.initialize_app(config)
