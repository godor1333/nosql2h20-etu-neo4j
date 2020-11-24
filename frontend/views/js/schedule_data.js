var xhr = new XMLHttpRequest();

var serverUrl = "http://" + window.location.hostname + ":8000";
var frontendUrl = "http://" + window.location.hostname + ":3000";

xhr.open('GET', frontendUrl.concat('/current/employee/id'), false);
xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();

var currentEmployeeId = xhr.responseText;

xhr.open('GET', frontendUrl.concat('/current/employee/name'), false);
xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();

var currentEmployeeName = xhr.responseText;

xhr.open('GET', frontendUrl.concat('/current/schedule/id'), false);
xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();

var currentDisciplineId = xhr.responseText;

xhr.open(
    'GET',
    serverUrl.concat("/employees/")
             .concat(currentEmployeeId)
             .concat("/schedule/?discipline_id=")
             .concat(currentDisciplineId),
    false
);

xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();

var data=JSON.parse(xhr.responseText);

var discipline = document.getElementById("discipline");
discipline.innerText = data.discipline.name;

var teacherName = document.getElementById("name");
teacherName.innerText = currentEmployeeName;

var table = document.getElementById("tab_body");
for (let i=0; i<data.lessons.length; i++){
    var tableTr = document.createElement("tr");
    table.appendChild(tableTr);

    var tableTdGroup = document.createElement("td");
    tableTr.appendChild(tableTdGroup);
    tableTdGroup.scope = "row";
    tableTdGroup.innerText = data.lessons[i].group;

    var tableTdTime = document.createElement("td");
    tableTr.appendChild(tableTdTime);
    tableTdTime.innerText = data.lessons[i].time;

    var tableTdAuditorium = document.createElement("td");
    tableTr.appendChild(tableTdAuditorium);
    tableTdAuditorium.innerText = data.lessons[i].auditorium;

}