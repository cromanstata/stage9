var now = (new Date()).getTime();
var lastTime = 0;
var lastTimeStr = localStorage['lastTime'];
var height = $('#box').height();
var width = $('#box').width();
if (lastTimeStr) lastTime = parseInt(lastTimeStr, 10);
if (now - lastTime > 20*24*1000) {
     // do animation
function flicker(count, callback, current) {

    current = current || 0;

    $("#box")[current % 2 == 0 ? 'hide' : 'show']();

    setTimeout(function(){
        if (count * 2 <= current) {
            callback();
            return;
        }
        flicker(count, callback, current + 1)
    }, 200*Math.random());
}

setTimeout(function () {
    flicker(7, function () {
        $("#box").fadeIn("slow");
        $("#box2").fadeIn("slow");
    })
}, 1000)

}
localStorage['lastTime'] = ""+now;

function tog(divId) {
    $(divId).toggle();
}





