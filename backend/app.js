var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var mqtt = require('mqtt');
var app = express();

var histData = [];
var bananaStats = {fresh: 1, rotten: 1, green: 1};

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/receive', function(req, res) {
  var client = mqtt.connect('mqtt://192.168.0.10');
  client.on('connect', function(topic, message) {
    client.publish("esys/TBA/sensor/control1", "upload");
    client.subscribe('esys/TBA/sensor/data');
    console.log('Listening to ' + 'esys/TBA/sensor/data');
  });
  var channel = req.query.channel;
  client.on('message', function(channel, msg) {
    message = String.fromCharCode.apply(null, msg);
    histData.push(message);

    console.log('Got message ' + message);
    console.log(message);
    
    res.send(histData);
    client.end();
  });
});

app.get("/eaten", function(req, res) {
  console.log("entered EATEN");

  var lastStatus = req.query.status;
  if (lastStatus == "Yellow") {
    bananaStats["fresh"] ++;
  } else if (lastStatus == "Brown") {
    bananaStats["rotten"] ++;
  } else if (lastStatus == "Green") {
    bananaStats["green"] ++;
  }
  console.log(bananaStats);

  histData = [];
  console.log("hist data reset");

  res.send(bananaStats);

});

app.get('/control', function(req, res) {
  var client = mqtt.connect('mqtt://192.168.0.10');
  client.on('connect', function(topic, message) {
    // client.subscribe('esys/TBA/x');
    console.log('Connected to MQTT')
    var command = req.query.cmd;
    client.publish('esys/TBA/sensor/control1', command);
    res.send('Success');
    client.end();
  });
});

app.get('/', function(req, res) {res.render('index')});
// app.get('/communication', function(req, res) {
//   var val = req.query.result;
//   // In his case he uses the 'craig' which inside the request
//   res.send(val);
// });

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

app.listen(3000)
module.exports = app;
