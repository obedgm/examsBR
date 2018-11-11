from classes import User, Folder, Section, Question
import classesUtils as cu

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
        folder = Folder("Historia 1", folderId)
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

        q2 = Question("Cuales son las intersecciones en x de la ecuacion [a]x^2 + [b]x + [c]", True)
        #q2.setFormula("(- b + sqrt(pow(b,2) - (4 * a * c)) / 2 * a) | a = rango(1,2) / b = rango(1,10) / c = rango(1,2)")

        q2.setFormula("(- b + sqrt(pow(b,2) - 4 * a * c)) / (2 * a) | a = rango(1,2) / b = rango(1,10) / c = rango(1,2)")

        s1 = Section("Porfiriato")
        s1.addQuestion(q1)
        s1.addQuestion(q2)
        # end mock data

        e1.addSection(s1)

    def updateUserData(self, user):
        # Actualizar al usuario y todo su desmadre
        return 0

    def getUserFiles(self, user):

        folders = {}

        folders["Historia 1 - fecha"] = "<p class=\"no-print\" style=\"color:green\">   Para imprimir da click en ctrl+P        </p>        <p class=\"no-print\" style=\"color:green\">            Para guardar da click en ctrl-P y selecciona \"Guardar como PDF en la lista de dispositivos\"     </p>        <br>                                <div style=\"page-break-after: always\">              <p>Examen: Historia 1</p>   <p>#1</p>               <p>Nombre:_______________________________________________________</p>               <p>Matricula:______________________________________________________</p>             <br>    <div id=\"questions_0\">              1. Que paso?<br><blockquote>a. Distractor2<br>b. Distractor3<br>c. Distractor1<br>d. Correcto<br></blockquote><br>2. Cuales son las intersecciones en x de la ecuacion 1x^2 + 4x + 1<br><blockquote>a. -0.268<br>b. -0.234<br>c. -0.258<br>d. -0.209<br></blockquote><br></div></div>                               <div style=\"page-break-after: always\">              <p>Examen: Historia 1</p>   <p>#2</p>               <p>Nombre:_______________________________________________________</p>               <p>Matricula:______________________________________________________</p>             <br>    <div id=\"questions_1\">              1. Cuales son las intersecciones en x de la ecuacion 2x^2 + 4x + 1<br><blockquote>a. -0.293<br>b. -0.5<br>c. -0.586<br>d. -0.219<br></blockquote><br>2. Cuales son las intersecciones en x de la ecuacion 1x^2 + 4x + 1<br><blockquote>a. -0.314<br>b. -0.268<br>c. -0.382<br>d. -0.114<br></blockquote><br></div>          </div>          <p>Solucion al examen: Historia 1</p>           <p>Version #1</p>   <div id=\"solutions_0\">                          1. d<br>2. a<br></div>          <br>                        <p>Solucion al examen: Historia 1</p>           <p>Version #2</p>   <div id=\"solutions_1\">                          1. a<br>2. b<br></div>          <br>"

        return folders