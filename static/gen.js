// Funciones para la generacion de examenes.

var correct = []

function displayQuestions(qNumber) {
	var contents = $("#contents").data().name;
	for (var x = 1; x < contents.length; x++) {
			var section = contents[x];
			var qLength = section["qLength"];
			var questions = section["questions"];
			questions.sort(function() { return 0.5 - Math.random() });
			for (var i = 0; i < qLength; i++) {
				question = questions[i];
				var qDisplay = String(correct.length+1) +  ". " + question['statement'] + "<br>";
				var answers = question['answers'];
				answers.sort(function() { return 0.5 - Math.random() });
				qDisplay += "<blockquote>";
				for (var j = 0; j < answers.length; j++) {
					var answer = answers[j];
					for (var key in answer) {
						if (key == "correct") {
							correct.push(String.fromCharCode('a'.charCodeAt(0) + j));
						}
						qDisplay += String.fromCharCode('a'.charCodeAt(0) + j) + ". " + String(answer[key]) + "<br>";
					}
				}
				qDisplay += "</blockquote>";
				qDisplay += "<br>";
				document.getElementById('questions_'+String(qNumber)).innerHTML += qDisplay;
			}
		}
}

function displaySolutions(sNumber) {
	var sDisplay = ""
	for (var x = 0; x < correct.length; x++) {
		sDisplay += String(x+1) + ". " + correct[x] + "<br>";
	}
	document.getElementById('solutions_'+String(sNumber)).innerHTML += sDisplay;
}

function submitData() {
	var folderName = $("#folderName").data()["name"];
	file = document.getElementById("file");
	date = Date(Date.now());
	var f = document.createElement("form");
	f.setAttribute('method',"post");
	f.setAttribute('action',"saveFile");
    var inputN = document.createElement("input");
    inputN.type = "text";
    inputN.name = "fileName";
    inputN.value = folderName + " - " + String(date.toString());
    f.appendChild(inputN);
    var inputD = document.createElement("input");
    inputD.type = "text";
    inputD.name = "fileContent";
    inputD.value = String(file.innerHTML.trim());
    f.appendChild(inputD);
    f.style.display = "none";
	document.body.appendChild(f);
	f.submit();
}

function genExams() {
	var contents = $("#contents").data().name;
	exams = parseInt(contents[0]);
	for (var k = 0; k < exams; k++){
		correct = [];
		displayQuestions(k);
		displaySolutions(k);
	}

	submitData();
}
