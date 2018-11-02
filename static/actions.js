function redirectMain() {
	var f = document.createElement("form");
	f.setAttribute('method',"post");
	f.setAttribute('action',"main");

    var userName = document.createElement("input");
    userName.type = "text";
    userName.name = "userName";
    userName.value = "usuario";

    var userId = document.createElement("input")
    userId.type = "text";
    userId.name = "userId";
    userId.value = "1";

    var email = document.createElement("input")
    email.type = "text";
    email.name = "email";
    email.value = "hola@hola.com";

    f.appendChild(userName);
    f.appendChild(userId);
    f.appendChild(email);
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
    var form = document.getElementById("createEvalForm");
    var name = form["name"].value;
    var errorMssg = document.getElementById("nameError");
    if (name.length <= 5 || name.length > 30) {
        errorMssg.innerHTML = "* El nombre debe ser de entre 5 y 30 caracteres";
    } else {
        form.submit();
    }
}

/*
function countQuestions() {
    var x = document.querySelectorAll(".example");
}
*/

var Saved = true;
var CountQuestions = 0;
function addQuestion() {
    var questionFormat = document.getElementById("questionFormat");
    $("#editor").append(questionFormat.innerHTML);
    CountQuestions++;
    Saved = false;
}

function toggleQuestion(checkbox, formula, answers) {
    if (checkbox.checked) {
        answers.style.display = "none";
        formula.style.display = "block";
    } else {
        answers.style.display = "block";
        formula.style.display = "none";
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

var clickSave = false;
function save() {
    document.getElementById("messageError").innerHTML = "";
    var elements = document.getElementById("editor").elements;
    var form = document.getElementById("editor");
    var save = true;
    var errorMssg = document.getElementById("messageError");
    var reject;

    for (var i = 0, element; element = elements[i++];) {
        element.classList.remove("emptyField");
        
        if (element.type == "checkbox") {
            if (element.checked) {
                reject = "answer";
            } else {
                reject = "formula";
            }
        } else if (element.type == "textarea" || 
                   element.type == "text" && 
                   element.value == "" &&
                   !element.classList.contains(reject)) {
            element.classList.add("emptyField");
            errorMssg.innerHTML = "* Hay campos vacios.";
            save = false;
        }
    }

    if (save) {
        clickSave = true;
        form.submit();
    }
}

function generateExams() {
    var form = document.getElementById("generateExamsForm");
    var errorMssg = document.getElementById("generateExamsError");
    var successMssg = document.getElementById("generateExamsSuccess");
    if (!Saved || form["exams"].value < 1 || form["reactivos"].value < 1) {
        errorMssg.innerHTML = "* Guarde primero los cambios";
    } else {
        errorMssg.innerHTML = "";
        successMssg.innerHTML = "Exportando... Revisa tu correo.";
        setTimeout(function() {
            form.submit();
        }, 3000);
    }
}

window.onbeforeunload = function() {
    if (Saved || clickSave){
        return null;
    }
    return true;
};