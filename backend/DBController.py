from classes import User, Evaluation, Question
import classesUtils as cu

class DBController:

    def getOrCreateUser(self, userName, userId, email):
        # Busca en la BD el usuario y si no lo crea
        # Toma el output de la BD y en otra funcion 
        #   lo restructura a clases

        user = User(userName, userId, email)
        
        return user

    def getEvaluations(self, user):
        user.clearEvaluations()
        # Trae desde la base de datos todas las 
        #   evaluaciones del usuario y las agrega
        #   al usuario
        e1 = Evaluation("Eval 1", "Eval1")
        user.addEvaluation(e1)

    def addEvaluation(self, user, evalName, evalId):
        evaluation = Evaluation(evalName, evalId)
        user.addEvaluation(evaluation)
        # Guarda la evaluacion en la BD

    def getEvaluation(self, user, evalId):
        # Trae la evaluacion de la bd y se la pone
        #   al usuario
        evaluation = Evaluation("nombre", evalId)
        user.addEvaluation(evaluation)

    def getQuestions(self, user, evalId):
        user.clearEvaluations()
        self.getEvaluation(user, evalId)
        # Trae las preguntas desde la bd y se las
        #   pone a la evalaucion y al usuario
        
        q1 = Question("Que paso?", False)
        q1.setCorrect("Correcto")
        q1.addDistractor("Distractor1")
        q1.addDistractor("Distractor2")
        q1.addDistractor("Distractor3")

        q2 = Question("Que paso pt2?", True)
        q2.setFormula("X + Y")

        e1 = user.getEvaluation(evalId)
        e1.addQuestion(q1)
        e1.addQuestion(q2)


    def updateUserData(self, user):
        # Actualizar al usuario y todo su desmadre
        return 0
