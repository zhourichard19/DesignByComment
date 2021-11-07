let totalFocussed = 0;
let totalDistractions = 0;
var intervalID = setInterval(function(){
    $.get( "/distractionCount", function( data ) {
        console.log(data);
        totalFocussed += data.prediction;
        totalDistractions += Math.abs(data.prediction-1);
        $( ".prediction" ).html("Focussed: "+totalFocussed+", Distractions: "+totalDistractions);
      });
}, 100);