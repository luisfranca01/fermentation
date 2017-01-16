alert("sda");
console.log("dsadsa");

var runState; // para identificar se a corrida está on a partir do python. Apagar abaixo se nao se usar esta var.

$(function(){
   $('#runButton').click(function() {
      if ((this).text==="Stop" || runState) {
         (this).text = "Start"; runState=false; $ ('#toplabel').text("Stopped"); $ ("#runButton").removeClass("btn-warning btn-danger").addClass("btn-success");
      } else {(this).text="Stop"; runState=true; $ ('#toplabel').text("Running"); $ ("#runButton").removeClass("btn-warning btn-success").addClass("btn-danger active");}
      console.log(runState)
   })

});

//datePeriod
$(function() {
  $('input[name="daterange"]').daterangepicker();
});

google.load('visualization', '1', {packages: ['corechart']});
google.setOnLoadCallback(drawChart);
function drawChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'Data');
  data.addColumn('number', 'T1');
  data.addColumn('number', 'T2');
  data.addColumn('number', 'Texterior');
  data.addRows([
   {% for row in records %}
   [new Date({{row[0][0:4]}},{{row[0][5:7]}},{{row[0][8:10]}},{{row[0][11:13]}},{{row[0][14:16]}}),
   {{'%0.2f'|format(row[1])}},
   {{'%0.2f'|format(row[2])}},
   {{'%0.2f'|format(row[3])}}],
   {% endfor %}
   ]);

  var options = {
    width: 600,
    height: 563,
    hAxis: {
      title: "Data",
      gridlines: { count: {{records_items}}, color: '#CCC' },
      format: 'dd-MMM-yyyy HH:mm' },
      vAxis: {
         title: 'ºC'
      },
      title: 'Temperatura',
    curveType: 'function'  //Makes line curved
 };
 var chart = new google.visualization.LineChart(document.getElementById('chart_temps'));
 chart.draw(data, options);
}

//createRun
function createRun() {
var runName = prompt(, "New Run");
}

jQuery(document).ready(function() {
$('.dropdown').on('click','a[data-toggle="dropdown"]',
       function(){
         if($(this).children().length <= 0){
                 $(this).append( '<ul class="dropdown-menu" role="menu" aria-labelledby="dLabel" >'+ '<li><a href="#">Edit</a></li><li><a href="#">Report</a></li><li><a href="#">Delete</a></li></ul>' );
                $(this).dropdown();
                      }
                  });
});
var files = dbFiles;

var list = document.getElementById("fileList");
        for (var i = 0; i < files; i++){
            var opt = table.getValue(i, 0);
            var li = document.createElement("li");
            var link = document.createElement("a");
            var text = document.createTextNode(opt);
            link.appendChild(text);
            link.href = "#";
            li.appendChild(link);
            list.appendChild(li);
          }
