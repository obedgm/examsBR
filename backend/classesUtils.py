from classes import User, Evaluation, Question
import json

def formatEvaluations(user):
	evaluations = user.getEvaluations()
	formattedEvaluations = []
	for evaluation in evaluations:
		formattedEvaluations.append({
			'evalName' : evaluation.getName(),
			'evalId' : evaluation.getId()
		})
	return formattedEvaluations

def formatEvaluationsJSON(user):
	formattedEvaluations = formatEvaluations(user)
	formattedEvaluationsJSON = json.dumps(formattedEvaluations)
	return formattedEvaluationsJSON

def getEvalName(user, evalId):
	evaluations = user.getEvaluations()
	for e in evaluations:
		if e.getId() == evalId:
			return e.getName()

def getFormattedQuestions(user, evalId):
	formattedQuestions = []
	evaluations = user.getEvaluations()
	for e in evaluations:
		if e.getId() == evalId:
			questions = e.getQuestions()
			for q in questions:
				if q.getAlgebraic():
					formattedQuestions.append({
						'algebraic' : 'true',
						'statement' : q.getStatement(),
						'formula' : q.getFormula()
					})
				else:
					distractors = q.getDistractors()
					formattedQuestions.append({
						'statement' : q.getStatement(),
						'correct' : q.getCorrect(),
						'distractor1' : distractors[0],
						'distractor2' : distractors[1],
						'distractor3' : distractors[2]
					})
	return formattedQuestions

def saveEvaluation(form, user, evalId):
	return 0;