// Funciones para la interaccion con el editor de materias.

function countIds() {
    var s_id = 0;
    var q_id = 0;
    var children = document.getElementById("editor").children;
    for (var i = 0, child; child = children[i++];) {
        if (child.classList.contains("section")){
            q_id = 1;
            s_id = s_id + 1;
            child.id = s_id;
        } else if (child.classList.contains("question")) {
            child.id = s_id + "_" + q_id;
            q_id = q_id + 1;
        }
    }
}
function displayedCounts() {
    var questions = document.querySelectorAll(".question");
    var counter = document.getElementById("countQuestions");
    counter.innerHTML = questions.length -1;

    var s = 0;
    var q;
    var children = document.getElementById("editor").querySelectorAll("*");
    for (var i = 0, child; child = children[i++];) {
        if (child.classList.contains("sectionNumber")){
            q = 1;
            s = s + 1;
            child.innerHTML = s;
        } else if (child.classList.contains("questionNumber")) {
            child.innerHTML = s + "." + q;
            q = q + 1;
        }
    }
}
function countElements() {
    countIds();
    displayedCounts();
}

var Saved = true;

function addQuestion() {
    var questionFormat = document.getElementById("questionFormat");
    $("#editor").append(questionFormat.innerHTML);
    Saved = false;
    countElements();

    question = document.getElementById("editor").lastElementChild;
    animate(question);
}

function addSection() {
    var sectionFormat = document.getElementById("sectionFormat");
    $("#editor").append(sectionFormat.innerHTML);
    Saved = false;
    countElements();

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
    Question.remove();
    countElements();
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
            question.remove();
        }
    }

    Section.remove();

    countElements();
    animate(form);
}

function moveQuestionUp(question) {
    var sectionId = question.id.substr(0, question.id.indexOf("_"));
    var section = document.getElementById(sectionId);

    if (sectionId != "1") {
        $(question.id).detach();
        question.parentNode.insertBefore(question, section);
        countElements();
        animate(section);
        animate(question);
    }
}

function moveQuestionDown(question) {
    var sectionId = String(parseInt(question.id.substr(0, question.id.indexOf("_")))+1);
    var section = document.getElementById(sectionId);
    var form = document.getElementById("editor");
    next = section.nextElementSibling;

    var sections = document.querySelectorAll(".section");
    if (sectionId != String(sections.length)) {
        if (next != null) {
            $(question.id).detach();
            question.parentNode.insertBefore(question, next);
        } else {
            $(question.id).detach();
            form.appendChild(question);
        }
        animate(section);
        animate(question);
        countElements();
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

    var sections = new Set();
    var duplicatedSections = new Set();
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
            errorMssg.innerHTML = "Hay campos vacios. ";
            save = false;
        } else if (element.name == "section") {
            if (sections.has(element.value)) {
                duplicatedSections.add(element.value);
            } 
            sections.add(element.value);
        }
    }

    if (duplicatedSections.size > 0) {
        errorMssg.innerHTML += "Hay nombres de seccion duplicados.";
        save = false;
        for (var i = 0, element; element = elements[i++];) {
            if (element.name == "section") {
                if (duplicatedSections.has(element.value)) {
                    element.classList.add("emptyField");
                }
            }
        }
    }

    if (save) {
        var s_id = 0;
        var q_id = 0;
        for (var i = 0, element; element = elements[i++];) {
            if (element.name == "section") {
                s_id = s_id + 1;
                element.name = s_id + "_" + element.name;
                q_id = 0;
            } else {
                if (element.name == "question") {
                    q_id = q_id + 1;
                }
                element.name = s_id + "_" + q_id + "_" + element.name;
            }
        }
        Saved = true;
        form.submit();
    } else {
        errorMssg.style.display = "block";
        successMssg.style.display = "none";
    }
}

function confirmUndoChanges() {
    var form = document.getElementById('folderData');
    Saved = true;
    form.submit();
}

function generateExams() {
    var sections = $("#sectionsData").data();
    var form = document.getElementById("generateExamsForm");
    var errorMssg = document.getElementById("generateExamsError");
    var successMssg = document.getElementById("generateExamsSuccess");
    var generate = true;

    errorMssg.style.display = "none";
    if (!Saved) {
        errorMssg.style.display = "block";
        errorMssg.innerHTML = "Guarde primero los cambios.";
        generate = false;
    } else {
        for (var i = 0; i < sections.name.length; i++) {
            element = form.elements[sections.name[i].sName];
            element.classList.remove("emptyField");
            if (element.value > sections.name[i].limit){
                errorMssg.style.display = "block";
                errorMssg.innerHTML = "Definiste mas preguntas de las que contiene la seccion.";
                element.classList.add("emptyField");
                generate = false;
            }
        }
    }

    if (generate) {
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