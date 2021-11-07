let totalFocussed = 0;
let totalDistractions = 0;
let percentageDistraction=0;
let percentageFocus=0
var intervalID = setInterval(function(){
    $.get( "/distractionCount", function( data ) {
        console.log(data);
        totalDistractions += data.prediction;
        totalFocussed += Math.abs(data.prediction-1);
        percentageDistraction=totalDistractions/(totalFocussed+totalDistractions);
        percentageFocus=totalFocussed/(totalFocussed+totalDistractions);
        var data = {
          labels: [ 'Focused','Distracted'],
          series: [totalFocussed,totalDistractions ]
        };
        var options = {
          labelInterpolationFnc: function(value) {
            return value[0]
          }
        };

        var responsiveOptions = [
          ['screen and (min-width: 640px)', {
            chartPadding: 30,
            labelOffset: 100,
            labelDirection: 'explode',
            labelInterpolationFnc: function(value) {
              return value;
            }
          }],
          ['screen and (min-width: 1024px)', {
            labelOffset: 80,
            chartPadding: 20
          }]
        ];

        new Chartist.Pie('.ct-chart', data, options, responsiveOptions);


        $( ".prediction" ).html("Focussed: "+totalFocussed+", Distractions: "+totalDistractions);
      });
}, 200);