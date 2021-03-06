'''
Modulo de utilidades.
Formatea los objetos para ser desplegados en la interfaz.
'''

from classes import User, Folder, Section, Question
import json

def formatFolders(user):
	folderuations = user.getFolders()
	formattedFolders = []
	for folder in folderuations:
		formattedFolders.append({
			'folderName' : folder.getName(),
			'folderId' : folder.getId()
		})
	return formattedFolders

def formatFoldersJSON(user):
	formattedFolders = formatFolders(user)
	formattedFoldersJSON = json.dumps(formattedFolders)
	return formattedFoldersJSON

def getFolderName(user, folderId):
	folder = user.getFolder(folderId)
	return folder.getName()

def getFormattedContents(user, folderId):
	formattedContents = []
	folder = user.getFolder(folderId)

	sections = folder.getSections()

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

def saveFolder(form, user, folderId):
	
	folder = user.getFolder(folderId)
	folder.clearSections()

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
		folder.addSection(section);
		s = s + 1

def hasAlgebraics(section):
	questions = section.getQuestions()
	for question in questions:
		if question.getAlgebraic():
			return True
	return False

def formatSections(user, folderId):
	folder = user.getFolder(folderId)
	sections = folder.getSections()
	formattedSections = []
	for section in sections:
		if hasAlgebraics(section):
			limit = len(section.getQuestions()) * 10
			if limit < 100:
				limit = 100
			formattedSections.append({
				'sName' : section.getName(),
				'qLength' : len(section.getQuestions()),
				'limit' : limit
			})
		else:
			formattedSections.append({
				'sName' : section.getName(),
				'qLength' : len(section.getQuestions()),
				'limit' : len(section.getQuestions())
			})
	return formattedSections

def formatSectionsJSON(user, folderId):
	formattedSections = formatSections(user, folderId)
	formattedSectionsJSON = json.dumps(formattedSections)
	return formattedSectionsJSON
