class User:

    def __init__(self, name, id, email):
        self.__name = name
        self.__id = id
        self.__email = email
        self.__evaluations = {}

    def addEvaluation(self, evaluation):
        self.__evaluations[evaluation.getId()] = evaluation

    def deleteEvaluation(self, evalId):
        del self.__evaluations[evalId]

    def getName(self):
        return self.__name

    def getId(self):
        return self.__id

    def getEmail(self):
        return self.__email

    def getEvaluation(self, evalId):
        return self.__evaluations[evalId]

    def getEvaluations(self):
        return self.__evaluations.values()

    def clearEvaluations(self):
        self.__evaluations = {}

class Evaluation:
    
    def __init__(self, name, id):
        self.__name = name
        self.__id = id
        self.__sections = []

    def addSection(self, section):
        self.__sections.append(section)

    def getName(self):
        return self.__name

    def getId(self):
        return self.__id

    def getSections(self):
        return self.__sections

    def clearSections(self):
        self.__sections = []

class Section:

    def __init__(self, name):
        self.__name = name
        self.__questions = []

    def addQuestion(self, question):
        self.__questions.append(question)

    def getName(self):
        return self.__name

    def getQuestions(self):
        return self.__questions

    def clearQuestions(self):
        self.__questions = []

class Question:

    def __init__(self, statement, algebraic):
        self.__statement = statement
        self.__algebraic = algebraic
        self.__distractors = []

    def setCorrect(self, correct):
        self.__correct = correct

    def addDistractor(self, distractor):
        self.__distractors.append(distractor)

    def setFormula(self, formula):
        self.__formula = formula

    def getAlgebraic(self):
        return self.__algebraic

    def getStatement(self):
        return self.__statement

    def getCorrect(self):
        return self.__correct

    def getDistractors(self):
        return self.__distractors

    def getFormula(self):
        return self.__formula