var serverUrl = "http://" + window.location.hostname + ":8000";
var frontendUrl = "http://" + window.location.hostname + ":3000";

var form = document.forms.namedItem("fileinfo");
form.addEventListener('submit', function(ev) {
    var oData = new FormData(form);
    var oReq = new XMLHttpRequest();
    oReq.open("POST", serverUrl.concat('/import_document/'), false);
    oReq.onload = function(oEvent) {
        if (oReq.status == 200) {
            alert("Успешно")
        } else {
            alert("Ошибка " + oReq.status + " при попытке загрузить файл");
        }
    };

    oReq.send(oData);
    ev.preventDefault();
}, false);

function exportFile() {
    window.location.replace(serverUrl.concat('/export_document/'));
}