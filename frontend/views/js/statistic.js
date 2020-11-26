var xhr = new XMLHttpRequest();

var serverUrl = "http://" + window.location.hostname + ":8000";
var frontendUrl = "http://" + window.location.hostname + ":3000";

xhr.open('GET', serverUrl.concat("/statisticparams/"), false);
xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
xhr.send();

var data=JSON.parse(xhr.responseText);
console.log(data);

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

var selectParams = document.getElementById("param");
for (let i=0; i<data.params.length; i++){
    var options = document.createElement("option");
    selectParams.appendChild(options);
    options.innerText = data.params[i].name;
}

function getStatistic() {
    var divChart = document.getElementById("divChart");
    divChart.innerHTML = "";
    var canvasEl = document.createElement("canvas");
    canvasEl.id = "chart";
    canvasEl.width = 600;
    canvasEl.height = 400;
    divChart.appendChild(canvasEl);
    var selectFaculties = document.getElementById("faculties");
    var facultyId = null;
    if (selectFaculties.selectedIndex > 0) {
        facultyId = data.faculties[selectFaculties.selectedIndex - 1].id
    }

    var selectDepartments = document.getElementById("department");
    var departmentId = null;
    if (selectDepartments.selectedIndex > 0) {
        departmentId = data.departments[selectDepartments.selectedIndex - 1].id
    }

    var selectParams = document.getElementById("param");
    var paramId = null;
    if (selectParams.selectedIndex > 0) {
        paramId = data.params[selectParams.selectedIndex - 1].id
    }

    var isExist = false;
    var url = serverUrl.concat("/statistic/");
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
        url = url.concat("department_id=").concat(departmentId);
    }

    if (paramId != null) {
        if (!isExist) {
            url = url.concat("?");
            isExist = true;
        } else {
            url = url.concat("&");
        }
        url = url.concat("param_id=").concat(paramId);
    }

    console.log(url);
    xhr.open(
        'GET',
        url,
        false
    );
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
    xhr.send();

    var statisticResponse=JSON.parse(xhr.responseText);
    console.log(statisticResponse);

    var labelEl = [];
    var dataEl = [];
    for (let i = 0; i < statisticResponse.length; ++i) {
        labelEl.push(statisticResponse[i].x);
        dataEl.push(statisticResponse[i].y);
    }


    var popCanvas = document.getElementById("chart");
    var barChart = new Chart(popCanvas, {
        type: 'bar',
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        },
        data: {
            labels: labelEl,
            datasets: [{
                label: 'Столбчатая диаграмма',
                data: dataEl,
            }]
        }
    });
}


var popCanvas = document.getElementById("chart");
var barChart = new Chart(popCanvas, {
    type: 'bar',
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    },
    data: {
        labels: [],
        datasets: [{
            label: 'Столбчатая диаграмма',
            data: [],
        }]
    }
});