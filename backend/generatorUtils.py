from classes import User, Folder, Section, Question
import json
from random import *
from math import *

def countAlgebraics(questions):
	count = 0
	for question in questions:
		if question.algebraic:
			count = count + 1

def generateAlgebraics(form, user, folderId):

	safe_dict_exec = {}
	safe_dict_exec['rango'] = randint
	safe_dict_exec['abs'] = abs
	safe_dict_exec['sqrt'] = sqrt
	safe_dict_exec['pow'] = pow

	requested = form['amount']

	folder = user.getFolder(folderId)

	sections = folder.getSections()

	for section in sections:

		questions = section.getQuestions()
		algebraics = countAlgebraics(questions)
		if algebraics > 0:
			return ""
			
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

				for x in range(0, 5):
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
				for x in range(0, ceil((requested - len(questions)) / algebraics)):
					try:
						correct = round(eval(formula, {"__builtins__":None}, safe_dict_exec), 3)
					except:
						correct = '#'
						pass

					q.setCorrect(correct)

					print('correct\n' + str(q.getCorrect()))

					for y in range(0, 3):

						for variable in variables:
							try:
								exec(variable.strip(), {"__builtins__":None}, safe_dict_exec)
								print("ya salio " + str(eval("a", {"__builtins__":None}, safe_dict_exec)))
							except:
								pass
						try:
							distractor = round(eval(formula, {"__builtins__":None}, safe_dict_exec), 3)
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
	formatContent.append(form["amount"])

	for section in sections:
		questions = section.getQuestions()
		formatQuestions = []
		for question in questions:
			formatQuestion = {}
			distractors = question.getDistractors()
			formatQuestion['statement'] = question.getStatement()

			formatAnswer = []

			formatAnswer.append({'correct' : question.getCorrect()})
			formatAnswer.append({'distractor1' : distractors[0]})
			formatAnswer.append({'distractor2' : distractors[1]})
			formatAnswer.append({'distractor3' : distractors[2]})

			formatQuestion['answers'] = formatAnswer

			formatQuestions.append(formatQuestion)
		formatSection = {
			'section' : section.getName(),
			'qLength' : form[section.getName()],
			'questions' : formatQuestions
		}
		formatContent.append(formatSection)

	formatContentJSON = json.dumps(formatContent)

	print(formatContent)
	print(formatContentJSON)

	return formatContentJSON
