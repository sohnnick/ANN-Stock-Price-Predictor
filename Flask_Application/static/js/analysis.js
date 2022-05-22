var results_hist = JSON.parse(document.getElementById('historical').innerHTML);
var results_ana = JSON.parse(document.getElementById('analysis').innerHTML);
var results_seven = JSON.parse(document.getElementById('next_seven_forecast').innerHTML);

document.getElementById('historical').innerHTML = '';
document.getElementById('analysis').innerHTML = '';
// document.getElementById('next_seven_forecast').innerHTML = '';

// create a chart
chart = anychart.line();

// *******************
// Line for next 7 days
// *******************
console.log(results_seven);
var keys = new Array();
for(var key in results_seven){
  keys.push(key)
};

var data_graph = [];

for(let i=0; i < keys.length; i++){

  var temp = keys[i];
  var temp_instance = [];
  temp_instance[0] = temp;
  temp_instance[1] = results_seven[temp];
  
  data_graph[i] = temp_instance;
};

var series_forecast = chart.line(data_graph);
series_forecast.name("Historical");

chart.title('Prediction for the Next 7 Days');
chart.xAxis().title('Date');
chart.yAxis().title('Stock Price');

// set the container id
chart.container("forecast_graph");

// initiate drawing the chart
chart.draw();

// create a chart
chart = anychart.line();

// *******************
// line for historical
// *******************
console.log(results_hist);
var keys = new Array();
for(var key in results_hist){
  keys.push(key)
};

var data_graph = [];

for(let i=0; i < keys.length; i++){

  var temp = keys[i];
  var temp_instance = [];
  temp_instance[0] = temp;
  temp_instance[1] = results_hist[temp];
  
  data_graph[i] = temp_instance;
};

var series_historical = chart.line(data_graph);
series_historical.name("Historical");

// *******************
// line for analysis
// *******************
var keys = new Array();
for(var key in results_ana){
  keys.push(key)
};

var data_graph = [];

for(let i=0; i < keys.length; i++){

  var temp = keys[i];
  var temp_instance = [];
  temp_instance[0] = temp;
  temp_instance[1] = results_ana[temp];
  
  data_graph[i] = temp_instance;
};

var series_analysis = chart.line(data_graph);
series_analysis.name("Prediction for Validation Set");

// chart attributes
chart.title('Performance of Model on Validation Set');
chart.xAxis().title('Date');
chart.yAxis().title('Stock Price');
chart.legend(true);

// set the container id
chart.container("container_graph");

// set colors
chart.palette(["Gray", "Black"]);

// initiate drawing the chart
chart.draw();
