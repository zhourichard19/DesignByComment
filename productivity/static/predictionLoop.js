let totalFocussed = 0;
let totalDistractions = 0;
let running = true;
var intervalID = setInterval(function () {
  $.get("/distractionCount", function (data) {
    console.log(data);
    totalFocussed += data.prediction;
    totalDistractions += Math.abs(data.prediction - 1);
    $(".prediction").html("Focussed: " + totalFocussed + ", Distractions: " + totalDistractions);
  });
}, 100);
$(".buttonReset").bind("click", function () {
  if (running) {
    clearInterval(intervalID);
    console.log("cleared");
  } else {
    console.log("TODO");
  }
  running = !running;
});