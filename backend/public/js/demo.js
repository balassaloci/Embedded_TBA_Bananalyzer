type = ['','info','success','warning','danger'];
    	
storage = [];
useJSON = true;

function updateLive() {
  var param = {channel: 'esys/TBA/sensor/data'};
  //$('#sensorData').html('Waiting...')
  $.get('/receive', param, function(data) {
    if (useJSON) {
      console.log('Received data: ' + data)
      jsonObject = data; //JSON.parse(data);
    } else {
      jsonObject = data;
    }
    save(data);
    //$('#sensorData').html('Data saved')
  });
}

$('#updateButton').on('click', function(e) {
  updateLive();
});

$('#eatenBananaButton').on('click', function(e) {
  var lastStatus = JSON.parse(storage[storage.length - 1])["Banana color"];

  var param = {status: lastStatus};
  $.get('/eaten', param, function(data) {
    //console.log(data);

    var totalNum = data["fresh"] + data["rotten"] + data["green"];
    
    Chartist.Pie('#chartPreferences', {
      labels: [Math.round(100 * data["fresh"] / totalNum, 0) + "%",
               Math.round(100 * data["rotten"] / totalNum, 0) + "%",
               Math.round(100 * data["green"] / totalNum, 0) + "%"],
      series: [data["fresh"], data["rotten"], data["green"]]
    });
    
    updateLive();
  });

  
});

// function replaceAndSplit(s, a, b) {
//   x = (""+x).replace('},{', '}|{');
//   xsplit = (""+x).split("|");

//   if (xsplit.length == 1) {
//     return xsplit[0];
//   } else {
//     return xsplit[0].concat(replaceAndSplit(xsplit[1], a, b));
//   }
// }

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};

function save(x) {
  // storage.push(x);
  x = (""+x).replaceAll('},{', '}|{');
  console.log(x);
  storage = (""+x).split("|");
  console.log(storage);
  // console.log('Storage is' + storage);
  updateChart(storage);
  // return storage.join("\n");
}

function updateChart(dta) {
  
  var xs = [];
  var ys = [];
  //console.log("FULL DATA");
  //console.log(dta);
  for (var i = 0 ; i < dta.length; i++) {
    //console.log("data line: " + dta[i]);
    jsonLine = JSON.parse(dta[i]);
    //console.log(jsonLine);
    //console.log(jsonLine["HSL Data"]);

    ys.push(jsonLine["Ripeness"]);
    xs.push(i);
  }

  var lastData = JSON.parse(dta[dta.length - 1]);
  //lastData = {'HSL Data':{'H':100,'S':45,'L':10}, 'Banana color': "Rotten", 'Time': "123"};
  var lastHsl = lastData["HSL Data"];
  var hslString = "hsl(" + lastHsl["H"] + "," + lastHsl["S"] + "%," + lastHsl["L"] + "%)";
  //alert(hslString);
  //hslString = "hsl(100, 50%, 50%)";
  //$("#colorName").css({"background-color": hslString});
  
  $("#colorName").css({"background": hslString });
  $("#colorName").text(lastData["Banana color"]);
  //var d = new Date(year, month, day, hours, minutes, seconds, milliseconds);
    var dataSales = {
      labels: xs,
      series: [
          ys
      ]
    };
    
    var optionsSales = {
      lineSmooth: false,
      low: 0,
      high: 100,
      showArea: true,
      height: "245px",
      axisX: {
        showGrid: false,
      },
      lineSmooth: Chartist.Interpolation.simple({
        divisor: 3
      }),
      showLine: false,
      showPoint: false,
    };
    
    var responsiveSales = [
      ['screen and (max-width: 640px)', {
        axisX: {
          labelInterpolationFnc: function (value) {
            return value[0];
          }
        }
      }]
    ];

    Chartist.Line('#chartHours', dataSales, optionsSales, responsiveSales);
    
}

demo = {
    initPickColor: function(){
        $('.pick-class-label').click(function(){
            var new_class = $(this).attr('new-class');  
            var old_class = $('#display-buttons').attr('data-class');
            var display_div = $('#display-buttons');
            if(display_div.length) {
            var display_buttons = display_div.find('.btn');
            display_buttons.removeClass(old_class);
            display_buttons.addClass(new_class);
            display_div.attr('data-class', new_class);
            }
        });
    },
    
    initChartist: function(){    
        
        var dataSales = {
          labels: [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
          series: [
             [93, 300, 59, 78, 24, 35, 73, 53, 82, 92, 15, 48, 20, 60, 82, 84, 94, 92, 2, 92]
          ]
        };
        
        var optionsSales = {
          lineSmooth: false,
          low: 0,
          high: 800,
          showArea: true,
          height: "245px",
          axisX: {
            showGrid: false,
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3
          }),
          showLine: false,
          showPoint: false,
        };
        
        var responsiveSales = [
          ['screen and (max-width: 640px)', {
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];
    
        Chartist.Line('#chartHours', dataSales, optionsSales, responsiveSales);
        
    
        var data = {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          series: [
            [542, 443, 320, 780, 553, 453, 326, 434, 568, 610, 756, 895],
            [412, 243, 280, 580, 453, 353, 300, 364, 368, 410, 636, 695]
          ]
        };
        
        var options = {
            seriesBarDistance: 10,
            axisX: {
                showGrid: false
            },
            height: "245px"
        };
        
        var responsiveOptions = [
          ['screen and (max-width: 640px)', {
            seriesBarDistance: 5,
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];
        
        Chartist.Bar('#chartActivity', data, options, responsiveOptions);
    
        var dataPreferences = {
            series: [
                [25, 30, 20, 25]
            ]
        };
        
        var optionsPreferences = {
            donut: true,
            donutWidth: 40,
            startAngle: 0,
            total: 100,
            showLabel: false,
            axisX: {
                showGrid: false
            }
        };
    
        Chartist.Pie('#chartPreferences', dataPreferences, optionsPreferences);
        
        Chartist.Pie('#chartPreferences', {
          labels: ['62%','32%','6%'],
          series: [62, 32, 6]
        });   
    },
    
    initGoogleMaps: function(){
        var myLatlng = new google.maps.LatLng(40.748817, -73.985428);
        var mapOptions = {
          zoom: 13,
          center: myLatlng,
          scrollwheel: false, //we disable de scroll over the map, it is a really annoing when you scroll through page
          styles: [{"featureType":"water","stylers":[{"saturation":43},{"lightness":-11},{"hue":"#0088ff"}]},{"featureType":"road","elementType":"geometry.fill","stylers":[{"hue":"#ff0000"},{"saturation":-100},{"lightness":99}]},{"featureType":"road","elementType":"geometry.stroke","stylers":[{"color":"#808080"},{"lightness":54}]},{"featureType":"landscape.man_made","elementType":"geometry.fill","stylers":[{"color":"#ece2d9"}]},{"featureType":"poi.park","elementType":"geometry.fill","stylers":[{"color":"#ccdca1"}]},{"featureType":"road","elementType":"labels.text.fill","stylers":[{"color":"#767676"}]},{"featureType":"road","elementType":"labels.text.stroke","stylers":[{"color":"#ffffff"}]},{"featureType":"poi","stylers":[{"visibility":"off"}]},{"featureType":"landscape.natural","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#b8cb93"}]},{"featureType":"poi.park","stylers":[{"visibility":"on"}]},{"featureType":"poi.sports_complex","stylers":[{"visibility":"on"}]},{"featureType":"poi.medical","stylers":[{"visibility":"on"}]},{"featureType":"poi.business","stylers":[{"visibility":"simplified"}]}]
    
        }
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);
        
        var marker = new google.maps.Marker({
            position: myLatlng,
            title:"Hello World!"
        });
        
        // To add the marker to the map, call setMap();
        marker.setMap(map);
    },
    
	showNotification: function(from, align){
    	color = Math.floor((Math.random() * 4) + 1);
    	
    	$.notify({
        	icon: "pe-7s-gift",
        	message: "Welcome to <b>Light Bootstrap Dashboard</b> - a beautiful freebie for every web developer."
        	
        },{
            type: type[color],
            timer: 4000,
            placement: {
                from: from,
                align: align
            }
        });
	}

    
}

