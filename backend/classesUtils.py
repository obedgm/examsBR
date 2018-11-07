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
	evaluation = user.getEvaluation(evalId)
	return evaluation.getName()

def getFormattedQuestions(user, evalId):
	formattedQuestions = []
	evaluation = user.getEvaluation(evalId)
	questions = evaluation.getQuestions()
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
	i = 1;
	evaluation = user.getEvaluation(evalId)
	evaluation.clearQuestions()
	while form.has_key(str(i) + '_question'):
		ii = str(i)
		if form.has_key(ii + '_algebra'):
			q = Question(form[ii+'_question'], True)
			print(form[ii+'_5'])
			q.setFormula(form[ii+'_5'])
		else:
			q = Question(form[ii+'_question'], False)
			q.setCorrect(form[ii+'_1'])
			q.addDistractor(form[ii+'_2'])
			q.addDistractor(form[ii+'_3'])
			q.addDistractor(form[ii+'_4'])
		evaluation.addQuestion(q)
		i = i + 1

