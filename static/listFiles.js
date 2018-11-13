// Permite la eliminacion de archivos del usuario.

var File;
function deleteFile(file) {
   	File = file;
    $("#deleteFileModal").modal("show");
}
function confirmDeleteFile() {
    form = document.getElementById("editor");
	var f = document.createElement("form");
	f.setAttribute('method',"post");
	f.setAttribute('action',"deleteFile");
    var input = document.createElement("input");
    input.type = "text";
    input.name = "fileName";
    input.value = File;
    f.appendChild(input);
    f.style.display = "none";
	document.body.appendChild(f);
	f.submit();
}
