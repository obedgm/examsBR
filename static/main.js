// Hssbilita y revisa la creacion de carpetas del usuario.

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
