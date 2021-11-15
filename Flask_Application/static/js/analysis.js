var results_hist = JSON.parse(document.getElementById('historical').innerHTML);
var results_ana = JSON.parse(document.getElementById('analysis').innerHTML);

document.getElementById('historical').innerHTML = '';
document.getElementById('analysis').innerHTML = '';

// create a chart
chart = anychart.line();
chart.title('Historical Item Quantity over Time');
chart.xAxis().title('Date');
chart.yAxis().title('Stock Price');

// line for historical
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

// line for analysis
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

// set the container id
chart.container("container_graph");

// set colors
chart.palette(["Blue", "Red"]);

// initiate drawing the chart
chart.draw();
