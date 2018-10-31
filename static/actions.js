function redirectMain() {
	var f = document.createElement("form");
	f.setAttribute('method',"post");
	f.setAttribute('action',"main");
    var input = document.createElement("input");
    input.type = "text";
    input.name = "user";
    input.value = "usuario";
    f.appendChild(input);
    f.style.display = "none";
	document.body.appendChild(f);
	f.submit();
}

/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    document.getElementById("homeNav").style.width = "250px";
    document.getElementById("content").style.marginLeft = "250px";
    document.getElementById("toggleBtn").onclick = closeNav;
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("homeNav").style.width = "0";
    document.getElementById("content").style.marginLeft = "0";
    document.getElementById("toggleBtn").onclick = openNav;
}

function createEval() {
    var form = document.getElementById("createEvalForm").submit();
    var name = form["name"];
    var errorMssg = document.getElementById("nameError").innerHTML;
    if (name.length < 5 || name.length > 30) {
        errorMssg = "El nombre debe ser de entre 5 y 30 caracteres";
    } else {
        form.submit();
    }
}

var Saved = true;
var CountQuestions = 0;
function addQuestion() {
    var formatoPregunta = document.getElementById("formatoPregunta");
    $("#editor").append(formatoPregunta.innerHTML);
    CountQuestions++;
    Saved = false;
}

function toggleQuestion(checkbox, answers) {
    if (checkbox.checked) {
        answers.style.display = "none";
    } else {
        answers.style.display = "block";
    }
    Saved = false;
}


var Question;
function deleteQuestion(question) {
    Question = question;
    $("#deleteQuestionModal").modal("show");
}
function confirmDeleteQuestion() {
    Question.innerHTML = "";
    Question.style.display = "none";
    CountQuestions--;
    Saved = false;
}

function save() {
    document.getElementById("messageError").innerHTML = "";
    var elements = document.getElementById("editor").elements;
    var form = document.getElementById("editor");
    var save = true;
    var errorMssg = document.getElementById("messageError");

    for (var i = 0, element; element = elements[i++];) {
        element.classList.remove("emptyField");
        if (element.type == "textarea" || element.type == "text" && element.value == "") {
            element.classList.add("emptyField");
            errorMssg.innerHTML = "* Hay campos vacios.";
            save = false;
        } else if (element.type == "checkbox") {
            if (element.checked) {
                i += 4;
            } 
        }
    }

    if (save) {
        form.submit();
    }
}

function generateExams() {
    var form = document.getElementById("generateExamsForm");
    var errorMssg = document.getElementById("generateExamsError");
    var successMssg = document.getElementById("generateExamsSuccess");
    if (Saved || form["exams"].value < 1 || form["reactivos"].value < 1) {
        errorMssg.innerHTML = "* Guarde primero los cambios";
    } else {
        errorMssg.innerHTML = "";
        successMssg.innerHTML = "Exportando... Revisa tu correo.";
        setTimeout(function() {
            form.submit();
        }, 3000);
    }
}
