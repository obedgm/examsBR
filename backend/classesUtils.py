from classes import User, Evaluation, Section, Question
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

def getFormattedContents(user, evalId):
	formattedContents = []
	evaluation = user.getEvaluation(evalId)

	sections = evaluation.getSections()

	for s in sections:
		formattedContents.append({
			'section' : s.getName(),
		})
		questions = s.getQuestions()
		for q in questions:
			if q.getAlgebraic():
				formattedContents.append({
					'algebraic' : 'true',
					'statement' : q.getStatement(),
					'formula' : q.getFormula()
				})
			else:
				distractors = q.getDistractors()
				formattedContents.append({
					'statement' : q.getStatement(),
					'correct' : q.getCorrect(),
					'distractor1' : distractors[0],
					'distractor2' : distractors[1],
					'distractor3' : distractors[2]
				})

	return formattedContents

def saveEvaluation(form, user, evalId):
	
	evaluation = user.getEvaluation(evalId)
	evaluation.clearSections()

	s = 1
	while form.has_key(str(s) + '_section'):
		ss = str(s)
		sectionName = form[ss + '_section']
		section = Section(sectionName)
		q = 1
		while form.has_key(ss + '_' + str(q) + '_question'):
			qq = str(q)
			if form.has_key(ss + '_' + qq + '_algebra'):
				question = Question(form[ss+'_'+qq+'_question'], True)
				question.setFormula(form[ss+'_'+qq+'_5'])
			else:
				question = Question(form[ss+'_'+qq+'_question'], False)
				question.setCorrect(form[ss+'_'+qq+'_1'])
				question.addDistractor(form[ss+'_'+qq+'_2'])
				question.addDistractor(form[ss+'_'+qq+'_3'])
				question.addDistractor(form[ss+'_'+qq+'_4'])
			section.addQuestion(question)
			q = q + 1
		evaluation.addSection(section);
		s = s + 1