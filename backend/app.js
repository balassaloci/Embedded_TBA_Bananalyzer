var express = require('express'),
    mqtt = require('mqtt'),
    swig = require('swig'),
    consolidate = require('consolidate'),
    schedule = require('node-schedule'),
    bodyParser = require('body-parser')

function connectMQTT() {
  var client = mqtt.connect('mqtt://192.168.0.10')

  client.on('connect', function() {
    // client.subscribe('esys/TBA')
    // client.publish('esys/TBA', 'A very long message')
    console.log('Connected to server')
  })

  client.on('message', function (topic, message) {
    console.log(message.toString())
    client.end()
  })
  return client;
}

var app = express();
app.locals.cache = 'memory';
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
// app.use(mqtt());
app.engine('html', consolidate.swig);
app.use(bodyParser());

app.get('/', function(req, res) {
  // var job = schedule.scheduleJob('5 * * * * *', function() {
  res.render('index.html', {userName: String(Math.random())});
})
app.post('/', function(req, res) {
  // res.send("Success");
  message = req.body.message
  channel = req.body.channel
  messageChannel = req.body.messageChannel
  client = connectMQTT()
  if (message !== "") {
    if (messageChannel === "") {
      messageChannel = 'esys/TBA';
    }
    client.publish(messageChannel, message)
  } else if (channel !== "") {
    console.log("Listening to:" + channel)
    client.subscribe(channel)
  }
  res.render('index.html', {userName: String(Math.random())});

});
// app.use(bodyParser())

app.listen(3000)
