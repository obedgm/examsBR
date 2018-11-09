function redirectMain() {
	var f = document.createElement("form");
	f.setAttribute('method',"post");
	f.setAttribute('action',"/login");

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
    var evaluations = $("#createEvalData").data();
    var form = document.getElementById("createEvalForm");
    form["evalName"].value = form["evalName"].value.trim();
    var name = form["evalName"].value;
    var errorMssg = document.getElementById("nameError");
    var submit = true;

    errorMssg.style.display = "none";
    if (name.length < 5 || name.length > 30) {
        errorMssg.style.display = "block";
        errorMssg.innerHTML = "El nombre debe ser de entre 5 y 30 caracteres";
        submit = false;
    } else {
        for (var i = 0; i < evaluations.name.length; i++) {
            if (name == evaluations.name[i].evalName) {
                errorMssg.style.display = "block";
                errorMssg.innerHTML = "Ya hay una evaluacion con ese nombre";
                submit = false;
            }
        }
    }

    if (submit) {
        form.submit();
    }
}

function countQuestions() {
    var questions = document.querySelectorAll(".question");
    var counter = document.getElementById("countQuestions");
    questionNumbers = document.querySelectorAll(".count");
    
    counter.innerHTML = questions.length -1;
    for (var i = 0, qn; qn = questionNumbers[i++];) {
        qn.innerHTML = i-1;
    }
    for (var i = 0, qi; qi = questions[i++];) {
        qi.id = i-1;
    }

}

var Saved = true;
function addQuestion() {
    var questionFormat = document.getElementById("questionFormat");
    $("#editor").append(questionFormat.innerHTML);
    Saved = false;
    countQuestions();
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
    Question.classList.add("animated");
    Question.classList.add("fadeOut");
    Saved = false;
    setTimeout(function(){ 
        Question.innerHTML = "";
        Question.classList.remove("question");
        countQuestions();
    }, 1000);
}

function moveQuestionUp(question) {
    if (question.id != 1) {
        beforeId = parseInt(question.id)-1;
        before = document.getElementById(beforeId);
        before.classList.remove("fadeIn");
        $(question.id).detach();
        question.parentNode.insertBefore(question, before);
        before.classList.add("fadeIn");
        Saved = false;
        countQuestions();
    }
}

function moveQuestionDown(question) {
    nextId = parseInt(question.id)+1;
    next = document.getElementById(nextId);    
    moveQuestionUp(next);
}

function save() {
    document.getElementById("messageError").innerHTML = "";
    var elements = document.getElementById("editor").elements;
    var form = document.getElementById("editor");
    var save = true;
    var errorMssg = document.getElementById("messageError");
    var reject;

    errorMssg.style.display = "none";
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
            errorMssg.style.display = "block";
            errorMssg.innerHTML = "Hay campos vacios.";
            save = false;
        }
    }

    if (save) {
        var id = 0;
        for (var i = 0, element; element = elements[i++];) {
            if (element.name == "question") {
                id = id + 1;
            }
            element.name = id + "_" + element.name;
        }

        Saved = true;
        form.submit();
    }
}

function confirmUndoChanges() {
    var form = document.getElementById('evalData');
    Saved = true;
    form.submit();
}

function generateExams() {
    var form = document.getElementById("generateExamsForm");
    var errorMssg = document.getElementById("generateExamsError");
    var successMssg = document.getElementById("generateExamsSuccess");

    form["exams"].classList.remove("emptyField");
    form["reactivos"].classList.remove("emptyField");
    errorMssg.style.display = "none";
    if (!Saved) {
        errorMssg.style.display = "block";
        errorMssg.innerHTML = "Guarde primero los cambios.";
    } else if (form["reactivos"].value < 1 || form["exams"].value < 1) {
        errorMssg.style.display = "block";
        errorMssg.innerHTML = "Especifique los valores faltantes.";
        if (form["reactivos"].value < 1) {
            form["reactivos"].classList.add("emptyField");
        }
        if (form["exams"].value < 1) {
            form["exams"].classList.add("emptyField");
        }
    } else {
        // TODO: Poner algun gif de carga en lo que carga la siguiente pagina
        form.submit();
    }
}

window.onbeforeunload = function() {
    if (Saved){
        return null;
    }
    return true;
};