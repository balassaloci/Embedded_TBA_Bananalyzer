storage = [];
useJSON = true;

$('#sendCommand').on('click', function(e) {
  var parameters = { cmd: 'upload' };
  $.get( '/control', parameters, function(data) {
    $('#status').html(data);
    // $('#sensorData').html(save(data));
  });
});

$('#updateButton').on('click', function(e) {
  var param = {channel: 'esys/TBA/sensor/data'};
  $('#sensorData').html('Waiting...')
  $.get('/receive', param, function(data) {
    if (useJSON) {
      jsonObject = JSON.parse(data);
    } else {
      jsonObject = data;
    }
    save(jsonObject);
    $('#sensorData').html('Data saved')
  });

});
function save(x) {
  storage.push(x);
  // return storage.join("\n");
}
