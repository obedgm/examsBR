'''
Modulo de utilidades.
Formatea las preguntas para la generacion de examenes y para su despliegue.
'''

from classes import User, Folder, Section, Question
import json
from random import *
from math import *
from sets import Set

def countAlgebraics(section):
	count = 0
	questions = section.getQuestions()
	for question in questions:
		if question.getAlgebraic():
			count = count + 1
	return count

def generateAlgebraics(form, user, folderId):

	safe_dict_exec = {}
	safe_dict_exec['rango'] = randint
	safe_dict_exec['abs'] = abs
	safe_dict_exec['sqrt'] = sqrt
	safe_dict_exec['pow'] = pow

	examsRequested = int(form['amount'])

	folder = user.getFolder(folderId)
	sections = folder.getSections()
	used = Set()
	s = 0
	for section in sections:
		s = s + 1
		algebraics = countAlgebraics(section)
		if algebraics == 0:
			return ""
		questions = section.getQuestions()
		q = 0
		for question in questions:
			questionsRequested = int(form[section.getName()])
			if question.getAlgebraic():
				q = q + 1
				error = 'Hay un error en la pregunta \'' + s + '.' + q + ": " + question.getStatement() + '\' <br>'
				data = question.getFormula()
				if (data.find('|') == -1):
					error += 'No se encontro el simbolo \'|\' que delimita las preguntas de las variables'
					return error
				formula = data[: data.find('|') - 1]
				rawVariables = data[data.find('|') + 1 :]
				while rawVariables.find(' ') != -1:
					rawVariables = rawVariables.replace(' ', '')
				variables = rawVariables.split('/')

				upperLimit = int(ceil((questionsRequested+1 - (len(questions)-algebraics)) / algebraics))*examsRequested
				if upperLimit <= 0:
					upperLimit = 2

				for x in range(0, upperLimit):
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

	return formatContentJSON
