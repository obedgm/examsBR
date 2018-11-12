function genExams() {
	var contents = $("#contents").data().name;
	console.log(contents);
	correct = [];
	exams = parseInt(contents[0]);
	console.log(exams);
	for (var k = 0; k < exams; k++){
		correct = []
		for (var x = 1; x < contents.length; x++) {
			section = contents[x];
			console.log(section);
			qLength = section["qLength"];
			console.log(qLength);
			questions = section['questions'];
			questions.sort(function() { return 0.5 - Math.random() });
			console.log(questions)
			for (var i = 0; i < qLength; i++) {
				question = questions[i];
				qDisplay = String(i+1) +  ". " + question['statement'] + "<br>";
				answers = question['answers'];
				answers.sort(function() { return 0.5 - Math.random() });
				qDisplay += "<blockquote>";
				for (var j = 0; j < answers.length; j++) {
					var answer = answers[j];
					for (var key in answer) {
						if (key == "correct") {
							correct[i] = String.fromCharCode('a'.charCodeAt(0) + j);
						}
						qDisplay += String.fromCharCode('a'.charCodeAt(0) + j) + ". " + String(answer[key]) + "<br>";
					}
				}
				qDisplay += "</blockquote>";
				qDisplay += "<br>";
				console.log(qDisplay);
				document.getElementById('questions_'+String(k)).innerHTML += qDisplay;
			}
		}
		console.log(correct);
	}
}
