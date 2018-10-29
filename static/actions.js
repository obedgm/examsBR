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
    document.getElementById("editor").innerHTML += document.getElementById("formatoPregunta").innerHTML;
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