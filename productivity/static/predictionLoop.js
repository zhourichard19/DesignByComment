let totalFrames = 0;
let totalDistractions = 0;
var intervalID = setInterval(function(){
    $.get( "/distractionCount", function( data ) {
        console.log(data);
        totalFrames+=1
        totalDistractions += Math.abs(data.prediction-1);
        $( ".prediction" ).html(data.prediction+","+totalDistractions);
      });
}, 100);