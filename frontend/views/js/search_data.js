var xhr = new XMLHttpRequest();

var serverUrl = "http://" + window.location.hostname + ":8000";
var frontendUrl = "http://" + window.location.hostname + ":3000";

xhr.open('GET', serverUrl.concat("/searchparams/"), false);
xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();

var data=JSON.parse(xhr.responseText);

var selectFaculties = document.getElementById("faculties");
for (let i=0; i<data.faculties.length; i++){
    var options = document.createElement("option");
    selectFaculties.appendChild(options);
    options.innerText = data.faculties[i].name;
}

var selectDepartment = document.getElementById("department");
for (let i=0; i<data.departments.length; i++){
    var options = document.createElement("option");
    selectDepartment.appendChild(options);
    options.innerText = data.departments[i].name;
}

var selectPosition = document.getElementById("position");
for (let i=0; i<data.jobs.length; i++){
    var options = document.createElement("option");
    selectPosition.appendChild(options);
    options.innerText = data.jobs[i];
}

var selectDegree = document.getElementById("academic_degree");
for (let i=0; i<data.degrees.length; i++){
    var options = document.createElement("option");
    selectDegree.appendChild(options);
    options.innerText = data.degrees[i].content;
}

function search() {
    var facultyId = null;
    var departmentId = null;
    var jobTitle = null;
    var degreeId = null;

    var selectFaculties = document.getElementById("faculties");
    if (selectFaculties.selectedIndex > 0) {
        facultyId = data.faculties[selectFaculties.selectedIndex - 1].id
    }

    var selectDepartment = document.getElementById("department");
    if (selectDepartment.selectedIndex > 0) {
        departmentId = data.departments[selectDepartment.selectedIndex - 1].id
    }

    var selectPosition = document.getElementById("position");
    if (selectPosition.selectedIndex > 0) {
        jobTitle = data.jobs[selectPosition.selectedIndex - 1];
    }

    var selectDegree = document.getElementById("academic_degree");
    if (selectDegree.selectedIndex > 0) {
        degreeId = data.degrees[selectDegree.selectedIndex - 1].id;
    }
    var isExist = false;

    var url = serverUrl.concat("/search/");
    if (facultyId != null) {
        if (!isExist) {
            url = url.concat("?");
            isExist = true;
        }
        url = url.concat("faculty_id=").concat(facultyId);
    }

    if (departmentId != null) {
        if (!isExist) {
            url = url.concat("?");
            isExist = true;
        } else {
            url = url.concat("&");
        }
        console.log(data.departments[departmentId]);
        url = url.concat("department_id=").concat(departmentId);
    }

    if (jobTitle != null) {
        if (!isExist) {
            url = url.concat("?");
            isExist = true;
        } else {
            url = url.concat("&");
        }
        url = url.concat("job_title=").concat(jobTitle);
    }

    if (degreeId != null) {
        if (!isExist) {
            url = url.concat("?");
            isExist = true;
        } else {
            url = url.concat("&");
        }
        url = url.concat("degree_id=").concat(degreeId);
    }

    xhr.open(
        'GET',
        url,
        false
    );
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
    xhr.send();

    var searchResponse=JSON.parse(xhr.responseText);

    var searchResponseTable = document.getElementById("search_response");
    searchResponseTable.innerHTML = "";
    for (let i=0; i < searchResponse.length; ++i) {
        var tr = document.createElement("tr");
        searchResponseTable.appendChild(tr);

        var name = document.createElement("td");
        name.scope = "row";
        name.innerText = searchResponse[i].name;
        tr.appendChild(name);

        var faculty = document.createElement("td");
        faculty.innerText = searchResponse[i].faculty;
        tr.appendChild(faculty);

        var department = document.createElement("td");
        department.innerText = searchResponse[i].department;
        tr.appendChild(department);

        var job = document.createElement("td");
        job.innerText = searchResponse[i].job;
        tr.appendChild(job);

        var degree = document.createElement("td");
        degree.innerText = searchResponse[i].degree;
        tr.appendChild(degree);
    }

}