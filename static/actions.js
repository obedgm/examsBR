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

function createFolder() {
    var folder = $("#createFolderData").data();
    var form = document.getElementById("createFolderForm");
    form["folderName"].value = form["folderName"].value.trim();
    var name = form["folderName"].value;
    var errorMssg = document.getElementById("nameError");
    var submit = true;

    errorMssg.style.display = "none";
    if (name.length < 5 || name.length > 30) {
        errorMssg.style.display = "block";
        errorMssg.innerHTML = "El nombre debe ser de entre 5 y 30 caracteres";
        submit = false;
    } else {
        for (var i = 0; i < folder.name.length; i++) {
            if (name == folder.name[i].folderName) {
                errorMssg.style.display = "block";
                errorMssg.innerHTML = "Ya hay una folderuacion con ese nombre";
                submit = false;
            }
        }
    }

    if (submit) {
        form.submit();
    }
}

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

    /*var questionNumbers = document.querySelectorAll(".questionNumber");
    for (var i = 0, qn; qn = questionNumbers[i++];) {
        qn.innerHTML = i-1;
    }*/

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
            console.log(next);
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
    }
}

function confirmUndoChanges() {
    var form = document.getElementById('folderData');
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