/*function redirectMain() {
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
}*/

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
    counter.innerHTML = questions.length -1;


    var questionNumbers = document.querySelectorAll(".count");
    for (var i = 0, qn; qn = questionNumbers[i++];) {
        qn.innerHTML = i-1;
    }

    var s_id = 0;
    var q_id = 0;
    var children = document.getElementById("editor").children;
    for (var i = 0, child; child = children[i++];) {
        if (child.classList.contains("section")){
            s_id = s_id + 1;
            child.id = s_id;
        } else if (child.classList.contains("question")) {
            q_id = q_id + 1;
            child.id = s_id + "_" + q_id;
        }
    }
}

var Saved = true;

function addQuestion() {
    var questionFormat = document.getElementById("questionFormat");
    $("#editor").append(questionFormat.innerHTML);
    Saved = false;
    countQuestions();

    question = document.getElementById("editor").lastElementChild;
    animate(question);
}

function addSection() {
    var sectionFormat = document.getElementById("sectionFormat");
    $("#editor").append(sectionFormat.innerHTML);
    Saved = false;
    countQuestions();

    section = document.getElementById("editor").lastElementChild;
    animate(section);
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
    form = document.getElementById("editor");
    Saved = false;
    Question.classList.remove("question");
    Question.innerHTML = "";
    countQuestions();
    animate(form);
}

var Section;
function deleteSection(section) {
    Section = section;
    $("#deleteSectionModal").modal("show");
}
function confirmDeleteSection() {
    form = document.getElementById("editor");
    Saved = false;

    var questions = document.querySelectorAll(".question");
    for (var i = 0, question; question = questions[i++];){
        if (question.id.indexOf(Section.id + "_") == 0) {
            question.classList.remove("question");
            question.innerHTML = "";
        }
    }

    Section.classList.remove("section");
    Section.innerHTML = "";

    countQuestions();
    animate(form);
}

function moveQuestionUp(question) {
    var sectionId = question.id.substr(0, question.id.indexOf("_"));
    var section = document.getElementById(sectionId);

    if (sectionId != "1") {
        $(question.id).detach();
        question.parentNode.insertBefore(question, section);
        countQuestions();
        animate(section);
        animate(question);
    }
}

function moveQuestionDown(question) {
    var sectionId = String(parseInt(question.id.substr(0, question.id.indexOf("_")))+1);
    var section = document.getElementById(sectionId);

    var questions = document.querySelectorAll(".question");
    if (sectionId != String(questions.length)) {
        $(question.id).detach();
        question.parentNode.insertBefore(section, question);
        countQuestions();
        animate(section);
        animate(question);
    }
}

function save() {
    document.getElementById("messageError").innerHTML = "";
    var elements = document.getElementById("editor").elements;
    var form = document.getElementById("editor");
    var save = true;
    var errorMssg = document.getElementById("messageError");
    var successMssg = document.getElementById("messageSuccess")
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
            successMssg.style.display = "none";
            save = false;
        }
    }

    if (save) {
        var s_id = 0;
        var q_id = 0;
        for (var i = 0, element; element = elements[i++];) {
            if (element.name == "section") {
                s_id = s_id + 1;
                element.name = s_id + "_" + element.name;
                q_id = 1;
            } else {
                element.name = s_id + "_" + q_id + "_" + element.name;
                if (element.name == "question") {
                    q_id = q_id + 1;
                }
            }
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

function animate(element) {
    element.classList.add("animated");
    element.classList.add("fadeIn");
    setTimeout(function() {
        element.classList.remove("animated");
        element.classList.remove("fadeIn");
    }, 1000);
}