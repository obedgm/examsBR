from classes import User, Folder, Section, Question
import json
from random import *
from math import *

def generateAlgebraics(user, folderId):

	safe_dict_exec = {}
	safe_dict_exec['rango'] = randint
	safe_dict_exec['abs'] = abs
	safe_dict_exec['sqrt'] = sqrt
	safe_dict_exec['pow'] = pow

	folder = user.getFolder(folderId)

	sections = folder.getSections()

	for section in sections:

		questions = section.getQuestions()

		for question in questions:

			if question.getAlgebraic():

				data = question.getFormula()

				print('data\n' + data)

				formula = data[: data.find('|') - 1]

				rawVariables = data[data.find('|') + 1 :]

				print('raw variables\n' + rawVariables)

				while rawVariables.find(" ") != -1:
					rawVariables = rawVariables.replace(" ", "")
				variables = rawVariables.split('/')

				print('variables\n' + str(variables))

				for x in range(0, 4):
					for variable in variables:
						try:
							exec(variable.strip(), {"__builtins__":None}, safe_dict_exec)
						except:
							pass			

					statement = question.getStatement()

					while statement.find('[') != -1:
						var = statement[statement.find('[') + 1 : statement.find(']')]
						try:
							val = str(eval(var, {"__builtins__":None}, safe_dict_exec))
						except:
							val = '#'
							pass
						statement = statement.replace('[' + var + ']', 
							str(eval(val, {"__builtins__":None}, safe_dict_exec)))
						print(statement)

					q = Question(statement, False)

					print('statement\n' + q.getStatement())

					try:
						correct = eval(formula, {"__builtins__":None}, safe_dict_exec)
					except:
						correct = '#'
						pass

					q.setCorrect(correct)

					print('correct\n' + str(q.getCorrect()))

					for y in range(0, 2):

						for variable in variables:
							try:
								exec(variable.strip(), {"__builtins__":None}, safe_dict_exec)
								print("ya salio " + str(eval("a", {"__builtins__":None}, safe_dict_exec)))
							except:
								pass
						try:
							distractor = eval(formula, {"__builtins__":None}, safe_dict_exec)
						except:
							pass
						
						q.addDistractor(distractor)

					print(str(q.getDistractors()))

					section.addQuestion(q)

				questions.remove(question)

def formatForDynamicDisplay(form, user, folderId):
	folder = user.getFolder(folderId)
	sections = folder.getSections()

	formatContent = []

	for section in sections:
		questions = section.getQuestions()
		formatQuestions = []
		for question in questions:
			formatQuestion = {}
			distractors = question.getDistractors()
			formatQuestion['statement'] = question.getStatement()
			if question.getAlgebraic():
				formatQuestion['algebraic'] = 'true'
				formatQuestion['formula'] = question.getFormula()
			else:
				formatQuestion['correct'] = question.getCorrect()
				formatQuestion['distractor1'] = distractors[0],
				formatQuestion['distractor2'] = distractors[1],
				formatQuestion['distractor3'] = distractors[2]
			formatQuestions.append(formatQuestion)
		formatSection = {
			'section' : section.getName(),
			'amount' : form['amount'],
			'questions' : formatQuestions
		}
		formatContent.append(formatSection)

	formatContentJSON = json.dumps(formatContent)

	print(formatContent)
	print(formatContentJSON)

	return formatContentJSON
	