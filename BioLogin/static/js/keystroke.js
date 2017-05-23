var Dynamics = {}; //Namespace for times array and i variable
timebetween = 0;
var count = null;

//When the page loads, initialize variables
$( document ).ready(function() {
    Dynamics.times = [];
    Dynamics.i = 0;
});

$(".key-input").keydown(function(){
    timebetween = 0;
    count = setInterval(function(){
        timebetween++;
    }, 1);
});

//Calculate time between keyup and keydown
$(".key-input").keyup(function(evt){
    //While ENTER is not pressed
    clearInterval(count);
    Dynamics.times[Dynamics.i] = timebetween;
    console.log(Dynamics.times[Dynamics.i]);
    Dynamics.i++;
});

//When the user submits the form
$("#target").submit(function( event ) {
    //Calculate average of
    var total = 0;
    for(var j = 0; j < Dynamics.times.length; j++) {
      total += Dynamics.times[j];
    }
    var average = total / Dynamics.times.length;

    $('#avg').val(average);
});
