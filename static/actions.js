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
    form = document.getElementById("createEval").submit();
    name = form["name"];
    if (name.length < 5 || name.length > 30) {
        document.getElementById("nameError").innerHTML = "El nombre debe ser de entre 5 y 30 caracteres";
    } else {
        form.submit();
    }
}

function addQuestion() {
    $("#editor").append(document.getElementById("formatoPregunta").innerHTML);
}

function toggleQuestion(checkbox) {
    answersTable = checkbox.parentElement.parentElement.parentElement.nextElementSibling.firstChild;
    if (checkbox.checked) {
        answersTable.style.display = "none";
    } else {
        answersTable.style.display = "block";
    }
}

function deleteQuestion(button) {
    questionTable = button.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
    questionTable.innerHTML = "";
    questionTable.style.display = "none";
}

function save() {
    /*var textInputs = new Array();
    textInputs = document.getElementsByTagName('input');
    var textAInputs = new Array();
    textAInputs = document.getElementsByTagName('textarea');
    save = true;
    form = document.getElementById("editor");

    for (i = 0; i < textInputs.length; i++) { 
        if (textInputs[i].type == 'text') {
            table = textInputs[i].parentElement.parentElement.parentElement.parentElement.parentElement.style;
            console.log(table);
            if (textInputs[i].value == 0) {
                textInputs[i].classList.add("emptyField");
                document.getElementById("messageError").innerHTML =
                    "* Hay campos vacios.";
                    save = false;
            } else {
                textInputs[i].classList.remove("emptyField");
            }
        }
    }

    for (i = 0; i < textAInputs.length; i++) {
        console.log(textAInputs[i]);
        if (textAInputs[i].value == 0) {
            textAInputs[i].classList.add("emptyField");
            document.getElementById("messageError").innerHTML =
                "* Hay campos vacios.";
                save = false;
        } else {
            textAInputs[i].classList.remove("emptyField");
        }
    }



    /*
    if (save) {
        form.submit();
    }*/

    var elements = document.getElementById("editor").elements;

    for (var i = 0, element; element = elements[i++];) {
        if (element.type == "textarea" || element.type == "text" && element.value == "") {
            element.classList.add("emptyField");
            console.log("it's an empty textfield");
        }
            
    }
}