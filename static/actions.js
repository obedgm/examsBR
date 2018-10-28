function redirectMain() {
	var f = document.createElement("form");
	f.setAttribute('method',"post");
	f.setAttribute('action',"main");
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
    var form = document.getElementById("createEval").submit();
    var name = form["name"];
    if (name.length < 5 || name.length > 30) {
        document.getElementById("nameError").innerHTML = "El nombre debe ser de entre 5 y 30 caracteres";
    } else {
        form.submit();
    }
}

function addQuestion() {
    document.getElementById("editor").innerHTML += document.getElementById("formatoPregunta").innerHTML;
}