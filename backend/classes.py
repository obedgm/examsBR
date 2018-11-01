class User:

	def __init__(self, name, id, email):
		self.__name = name
		self.__id = id
		self.__email = email

	def addFolder(folder):
		self.__folders.append(folder)

class Folder:

	def __init__(self, name, id):
		self.__name = name
		self.__id = id

	def addQuestion(question):
		self.__questions.append(question)

class Question:

	def __init__(self, statement, algebraic):
		self.__statement = statement
		self.__algebraic = algebraic

	def setCorrect(correct):
		self.__correct = correct

	def addDistractor(distractor):
		self.__distractors.append(distractor)

	def setFormula(formula):
		self.__formula = formula