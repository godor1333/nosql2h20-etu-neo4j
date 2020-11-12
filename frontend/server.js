var express = require('express');
var app = express();

var path    = require("path");
var cors=require('cors');
var engines = require('consolidate');

app.use(express.static(path.join(__dirname, 'views')));
app.use(cors({origin:true,credentials: true}));

app.engine('html', engines.mustache);
var currentDepId = "0";
var currentDepName = "";

app.get('/', function(req, res){
    res.render('html/faculties.html');
});

app.get('/departments', function (req, res) {
    currentDepId = req.param("id");
    currentDepName = req.param("name");
    res.render('html/departments.html');
});

app.get('/departments', function (req, res) {
    res.render('html/departments.html');
});

app.get('/current/department/id', function (req, res) {
    res.send(currentDepId);
});

app.get('/current/department/name', function (req, res) {
    res.send(currentDepName);
});

app.get('/employee', function (req, res) {
    res.render('html/employee.html');
});

app.get('/header.html', function(req, res){
    res.render('html/header.html');
});

app.listen(3000);