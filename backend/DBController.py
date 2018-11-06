from classes import User, Evaluation, Question
import classesUtils as cu

class DBController:

    def getOrCreateUser(self, userName, userId, email):
        # Busca en la BD el usuario y si no lo crea
        # Toma el output de la BD y en otra funcion 
        #   lo restructura a clases

        #Temporal
        q1 = Question("Que paso?", False)
        q1.setCorrect("Correcto")
        q1.addDistractor("Distractor1")
        q1.addDistractor("Distractor2")
        q1.addDistractor("Distractor3")

        q2 = Question("Que paso pt2?", True)
        q2.setFormula("X + Y")

        e1 = Evaluation("Eval 1", "Eval1")
        e1.addQuestion(q1)
        e1.addQuestion(q2)

        user = User(userName, userId, email)
        user.addEvaluation(e1)
        #Fin temporal
        
        return user

    def updateUserData(self, user):
        # Actualizar al usuario y todo su desmadre
        return 0
