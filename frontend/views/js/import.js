var serverUrl;
var frontendUrl = "http://127.0.0.1:3000";
if (navigator.platform.toLowerCase().includes("win")) {
    serverUrl = "http://192.168.99.101:8000";
} else {
    serverUrl = "http://127.0.0.1:8000";
}

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
