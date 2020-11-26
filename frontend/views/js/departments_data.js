var xhr = new XMLHttpRequest();

var serverUrl = "http://" + window.location.hostname + ":8000";
var frontendUrl = "http://" + window.location.hostname + ":3000";

xhr.open('GET', frontendUrl.concat('/current/department/name'), false);
xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();

var currentDepartmentsName = xhr.responseText;

var pageTitle = document.getElementsByClassName("page_title");
pageTitle[0].innerHTML =  currentDepartmentsName;

xhr.open('GET', frontendUrl.concat("/current/department/id"), false);
xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();

var currentDepartmentsId = xhr.responseText;

searchQuery();

function searchQuery() {
    var searchQueryEl = document.getElementById("searchQuery");
    var url = serverUrl.concat("/searchquery/?department_id=")
        .concat(currentDepartmentsId)
        .concat("&query=")
        .concat(searchQueryEl.value);
    xhr.open(
        'GET',
        url,
        false
    );
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
    xhr.send();

    var data=JSON.parse(xhr.responseText);
    var content = document.getElementById("content");
    content.innerHTML = "";
    var container = document.createElement("div");
    container.classList.add("container");
    content.appendChild(container);

    for (var i = 0; i < data.length; i+=2) {
        var rowContent = document.createElement("div");
        rowContent.classList.add("row", "content");
        container.appendChild(rowContent);

        for (var j = 0; j < 2 && (i+j)<data.length; ++j) {
            var col6 = document.createElement("div");
            col6.classList.add("col-6");
            rowContent.appendChild(col6);

            var row = document.createElement("div");
            row.classList.add("row");
            col6.appendChild(row);

            var col3 = document.createElement("div");
            col3.classList.add("col-3");
            row.appendChild(col3);

            var img = document.createElement("img");
            img.classList.add("photo");
            col3.appendChild(img);
            img.src = data[i + j].photo_url;

            var col9 = document.createElement("div");
            col9.classList.add("col-9");
            row.appendChild(col9);

            var a = document.createElement("a");
            a.classList.add("name");
            a.href = "/employee?id=" + data[i + j].id;
            a.innerText = data[i + j].name;
            col9.appendChild(a);

            var p = document.createElement("p");
            p.classList.add("position");
            p.innerText = data[i + j].job_title;
            col9.appendChild(p);
        }
    }
}



