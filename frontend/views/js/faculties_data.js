var xhr = new XMLHttpRequest();

var serverUrl;
if (navigator.platform.toLowerCase().includes("win")) {
    serverUrl = "http://192.168.99.101:8000";
} else {
    serverUrl = "http://127.0.0.1:8000";
}

xhr.open('GET', serverUrl.concat('/departments/'), false);
xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();
if (xhr.status !== 200) {
    throw xhr.status;
}
var data = JSON.parse(xhr.responseText);
var accordion = document.getElementById('accordion');

for (var i=0; i<data.length; i++) {
    var rowDiv = document.createElement("div");
    rowDiv.classList.add("row");
    accordion.appendChild(rowDiv);

    var col11Div = document.createElement("div");
    col11Div.classList.add("col-11");
    rowDiv.appendChild(col11Div);

    var facultiesName = document.createElement("h4");
    col11Div.appendChild(facultiesName);
    var facultiesNameContent = document.createTextNode(data[i].name);
    facultiesName.appendChild(facultiesNameContent);

    var col1Div = document.createElement("div");
    col1Div.classList.add("col-1");
    rowDiv.appendChild(col1Div);

    var button = document.createElement("button");
    button.id = "button" + i;
    button.classList.add("btn", "btn-link");
    button.setAttribute("data-toggle", "collapse");
    button.setAttribute("data-target", "#collapse" + i);
    button.setAttribute("aria-expanded", "false");
    button.setAttribute("aria-controls", "collapse" + i);
    col1Div.appendChild(button);

    var span = document.createElement("span");
    span.classList.add("fa", "fa-plus");
    button.appendChild(span);

    var divCollapse = document.createElement("div");
    divCollapse.id = "collapse" + i;
    divCollapse.classList.add("collapse");
    accordion.appendChild(divCollapse);

    var ul = document.createElement("ul");
    divCollapse.appendChild(ul);

    for (var j = 0; j < data[i].departments.length; j++) {
        var li = document.createElement("li");
        ul.appendChild(li);
        var departmentNameContent = document.createTextNode(data[i].departments[j].name);
        li.appendChild(departmentNameContent);
    }

    collapse(i);
}

function collapse(id) {
    $(function() {
        $('#collapse'.concat(id)).on('hide.bs.collapse', function () {
            $('#button'.concat(id)).html('<span class="fa fa-plus"></span>');
        });
        $('#collapse'.concat(id)).on('show.bs.collapse', function () {
            $('#button'.concat(id)).html('<span class="fa fa-minus"></span>');
        });
    });

}