from classes import User, Folder, Section, Question
import json
from random import *
from math import *
from sets import Set

'''
* que la cantidad de algebraicas generadas sea de acuerdo a lo que pidio el usuario
* que el limite de preguntas a poner en el examen sea ilimitado si hay al menos
	una algebraica, si no que sea igual a la cantidad de preguntas en la seccion
* recibir el numero de la pregunta para desplegar el numero cuando hay error
'''

def generateAlgebraics(user, folderId):

	safe_dict_exec = {}
	safe_dict_exec['rango'] = randint
	safe_dict_exec['abs'] = abs
	safe_dict_exec['sqrt'] = sqrt
	safe_dict_exec['pow'] = pow

	folder = user.getFolder(folderId)
	sections = folder.getSections()
	used = Set()
	for section in sections:
		questions = section.getQuestions()
		for question in questions:
			if question.getAlgebraic():
				error = 'Hay un error en la pregunta \'' + question.getStatement() + '\' <br>'
				data = question.getFormula()
				if (data.find('|') == -1):
					error += 'No se encontro el simbolo \'|\' que delimita las preguntas de las variables'
					return error
				formula = data[: data.find('|') - 1]
				rawVariables = data[data.find('|') + 1 :]
				while rawVariables.find(' ') != -1:
					rawVariables = rawVariables.replace(' ', '')
				variables = rawVariables.split('/')
				for x in range(0, 5):
					try:
						correct = '#'
						limit = 100
						while correct == '#' and limit > 0:
							for variable in variables:
								try:
									exec(variable.strip(), {'__builtins__':None}, safe_dict_exec)
								except:
									error += 'Error de sintaxis en la declaracion \'' + variable.strip()
									return error		
							statement = question.getStatement()
							while statement.find('[') != -1:
								try:
									var = statement[statement.find('[') + 1 : statement.find(']')]
									val = str(eval(var, {'__builtins__':None}, safe_dict_exec))
								except:
									error += 'Error de sintaxis en la coloccacion de variables'
									return error	
								statement = statement.replace('[' + var + ']', 
									str(eval(val, {'__builtins__':None}, safe_dict_exec)))
							q = Question(statement, False)
							limit = limit - 1
							try:
								correct = round(eval(formula, {'__builtins__':None}, safe_dict_exec), 3)
							except:
								correct = '#'
								pass
					except:
						error += 'Error al ejecutar la formula'
						return error
					q.setCorrect(correct)
					used.add(correct)
					for y in range(0, 3):
						try:
							distractor = '#'
							limitD = 100
							while (distractor == '#' or distractor in used) and limit > 0:
								limitD = limitD - 1
								for variable in variables:
									exec(variable.strip(), {'__builtins__':None}, safe_dict_exec)
								try:
									distractor = round(eval(formula, {'__builtins__':None}, safe_dict_exec), 3)
								except:
									distractor = '#'
									pass
						except:
							error += 'Selecciona un rango mayor para las variables, el rango proporcionado no puede generar suficientes distractores diferentes'
							pass
						q.addDistractor(distractor)
						used.add(distractor)
					section.addQuestion(q)
				questions.remove(question)
	return ''

def formatForDynamicDisplay(form, user, folderId):
	folder = user.getFolder(folderId)
	sections = folder.getSections()

	formatContent = []
	formatContent.append(form['amount'])

	for section in sections:
		questions = section.getQuestions()
		formatQuestions = []
		for question in questions:
			if question.getAlgebraic():
				break;

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