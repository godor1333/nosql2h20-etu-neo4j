var xhr = new XMLHttpRequest();

var serverUrl;
var frontendUrl = "http://127.0.0.1:3000";
if (navigator.platform.toLowerCase().includes("win")) {
    serverUrl = "http://192.168.99.101:8000";
} else {
    serverUrl = "http://127.0.0.1:8000";
}

xhr.open('GET', frontendUrl.concat('/current/employee/id'), false);
xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();

var currentEmployeeId = xhr.responseText;

xhr.open('GET', frontendUrl.concat('/current/department/id'), false);
xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();

var currentDepartmentId = xhr.responseText;

xhr.open(
    'GET',
    serverUrl.concat("/employees/")
        .concat(currentEmployeeId)
        .concat("/?department_id=")
        .concat(currentDepartmentId),
    false
);
xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();

var data=JSON.parse(xhr.responseText);

var emplName = document.getElementsByClassName("employee_name");
emplName[0].innerText = data.name;

var emplPosition = document.getElementsByClassName("tab_position");
emplPosition[0].innerText = data.job_title;

var emplAcademicDegree = document.getElementsByClassName("tab_academic_degree");
var degreesCompose = String("");
for (let i=0; i<data.degrees.length; i++){
    degreesCompose = degreesCompose.concat(data.degrees[i].content);
    if (i != data.degrees.length - 1){
        degreesCompose = degreesCompose.concat(", ");
    }
}
emplAcademicDegree[0].innerText = degreesCompose;

var emplEmail = document.getElementsByClassName("tab_email");
emplEmail[0].innerText = data.email;

var emplDiscipline = document.getElementById("discipline_list");
var emplDisciplineImg = document.getElementById("discipline_img");
var emplDisciplineUl = document.createElement("ul");
emplDiscipline.appendChild(emplDisciplineUl);
for (let i=0; i<data.disciplines.length; i++){
    var emplDisceplineLi = document.createElement("li");
    emplDisciplineUl.appendChild(emplDisceplineLi);
    emplDisceplineLi.innerText = data.disciplines[i].discipline.name;

    var emplDisciplineImgA = document.createElement("a");
    emplDisciplineImg.appendChild(emplDisciplineImgA);
    emplDisciplineImgA.href = "/schedule?id=" + data.disciplines[i].discipline.id + "&name=" + data.name;
    var emplDisciplineImgIcon = document.createElement("img");
    emplDisciplineImgA.appendChild(emplDisciplineImgIcon);
    emplDisciplineImgIcon.src = "https://img.icons8.com/material-sharp/24/000000/visible.png";
}


var emplEducation = document.getElementsByClassName("education");
emplEducation[0].innerText = data.education;

var emplInterests = document.getElementsByClassName("interests");
if (data.interests.length){
    emplInterests[0].innerText = data.interests[0];
}

var emplPublications = document.getElementsByClassName("publications");
var emplPublicationsOl = document.createElement("ol");
emplPublications[0].appendChild(emplPublicationsOl);
for (let i=0; i <data.publications.length; i++){
    var emplPublicationsLi = document.createElement("li");
    emplPublicationsOl.appendChild(emplPublicationsLi);
    emplPublicationsLi.innerText = data.publications[i].content;
}

