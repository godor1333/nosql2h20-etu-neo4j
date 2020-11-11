var express = require('express');
var app = express();

var path    = require("path");
var engines = require('consolidate');

app.use(express.static(path.join(__dirname, 'views')));
app.engine('html', engines.mustache);

app.get('/', function(req, res){
    res.render('html/faculties.html');
});

app.listen(3000);