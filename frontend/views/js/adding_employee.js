var xhr = new XMLHttpRequest();
let request = {};

var serverUrl = "http://" + window.location.hostname + ":8000";
var frontendUrl = "http://" + window.location.hostname + ":3000";

xhr.open('GET', frontendUrl.concat('/current/department/name'), false);
xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();

var currentDepartmentsName = xhr.responseText;

xhr.open('GET', frontendUrl.concat('/current/department/id'), false);
xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();

var currentDepartmentId = xhr.responseText;

function addField() {
    var publications = document.getElementById("publications");
    var publicationInput = document.createElement("input");
    publicationInput.classList.add("publicationChild");
    publicationInput.type = "text";
    publicationInput.placeholder = "Публикация";
    publications.appendChild(publicationInput);
}

function save() {
    request = {};

    var name = document.getElementById("name");
    request.name = name.value;

    var imageUrl = document.getElementById("image_url");
    request.photo_url = imageUrl.value;

    var email = document.getElementById("email");
    request.email = email.value;

    var education = document.getElementById("education");
    request.education = education.value;

    request.department = currentDepartmentsName;

    var job_title = document.getElementById("position");
    request.job_title = job_title.value;

    var requestDisciplines = [];
    var discipline = {};
    var lesson = {};
    var disciplinesElements = document.getElementsByClassName("disciplineName");
    for (let i = 0; i < disciplinesElements.length; ++i) {
        discipline = {};
        discipline.discipline = {};
        discipline.discipline.name = {};
        console.log("parent");
        console.log(disciplinesElements[i].parentNode);
        discipline.discipline.name = disciplinesElements[i].value;
        discipline.lessons = [];
        lesson = {};

        var children = disciplinesElements[i].parentNode.children;
        for (let j = 0; j < children.length; ++j) {
            console.log(children[j]);
            if (children[j].classList.contains("row")) {
                lesson = {};
                lesson.group = children[j].childNodes.item(0).childNodes.item(0).value;
                lesson.time = children[j].childNodes.item(1).childNodes.item(0).value;
                lesson.auditorium = children[j].childNodes.item(2).childNodes.item(0).value;
                discipline.lessons.push(lesson);
            }
        }
        requestDisciplines.push(discipline);
    }
    request.disciplines = requestDisciplines;

    var academicDegree = document.getElementById("academic_degree");

    var degrees = academicDegree.value.split(", ");
    var responseDegrees = [];
    for (let i = 0; i < degrees.length; ++i) {
        responseDegrees.push({"content": degrees[i]})
    }
    request.degrees = responseDegrees;
    request.interests = [];

    var requestPublications = [];
    var firstPublication = document.getElementsByClassName("publication");
    var content = {};
    content.content = firstPublication[0].value;
    requestPublications.push(content);

    var publications = document.getElementsByClassName("publicationChild");
    for (let i = 0; i < publications.length; ++i) {
        content = {};
        content.content = publications[i].value;
        requestPublications.push(content);
    }
    request.publications = requestPublications;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', serverUrl.concat('/employees/'), false);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
    xhr.send(JSON.stringify(request));

    if (xhr.status != 200) {
        alert("Поправьте данные");
        alert(xhr.responseText);
    } else {
        window.location.replace(frontendUrl.concat('/departments?')
            .concat("id=")
            .concat(currentDepartmentId)
            .concat("&name=")
            .concat(currentDepartmentsName)
        );
    }
}

function addSchedule() {
    var scheduling = document.getElementById("scheduleDisc");
    var newRow = document.createElement("div");
    newRow.classList.add("row");
    scheduling.appendChild(newRow);

    var col5Div = document.createElement("div");
    col5Div.classList.add("col-5");
    newRow.appendChild(col5Div);

    var disciplines = document.createElement("div");
    disciplines.classList.add("disciplines", "col-4");
    newRow.appendChild(disciplines);

    var name = document.createElement("input");
    name.placeholder = "Название дисциплины";
    name.type = "text";
    name.style = "width: 110%";
    name.classList.add("disciplineName");
    disciplines.appendChild(name);

    var col2Div = document.createElement("div");
    col2Div.classList.add("col-2");
    newRow.appendChild(col2Div);

    var scheduleButton = document.createElement("button");
    scheduleButton.setAttribute("onclick", "addScheduleForDiscipline(this)");
    scheduleButton.classList.add("schedule");
    scheduleButton.innerText = "Расписание";
    col2Div.appendChild(scheduleButton);
}

function addScheduleForDiscipline(elem) {
    var children = elem.parentNode.parentNode.children;
    var disciplines;
    for (let i = 0; i < children.length; ++i) {
        if (children[i].classList.contains("disciplines")) {
            disciplines = children[i];
            break;
        }
    }

    var scheduleEl = document.createElement("div");
    scheduleEl.classList.add("row");
    disciplines.appendChild(scheduleEl);

    var groupEl = document.createElement("div");
    groupEl.classList.add("col-3");
    scheduleEl.appendChild(groupEl);

    var groupInput = document.createElement("input");
    groupInput.placeholder = "Группа";
    groupInput.type = "text";
    groupInput.classList.add("group");
    groupEl.appendChild(groupInput);

    var timeEl = document.createElement("div");
    timeEl.classList.add("col-6");
    scheduleEl.appendChild(timeEl);

    var timeInput = document.createElement("input");
    timeInput.placeholder = "Время";
    timeInput.type = "text";
    timeInput.classList.add("time");
    timeEl.appendChild(timeInput);

    var audienceEl = document.createElement("div");
    audienceEl.classList.add("col-3");
    scheduleEl.appendChild(audienceEl);

    var audienceInput = document.createElement("input");
    audienceInput.placeholder = "Аудитория";
    audienceInput.type = "text";
    audienceInput.classList.add("audience");
    audienceEl.appendChild(audienceInput);
}

$(document).ready(function(){
    PopUpHide();
});
function PopUpShow(){
    $("#popup1").show();
}
function PopUpHide(){
    $("#popup1").hide();
}
