$(document).ready(function(){
    stopSearchBox();
});

function stopSearchBox() {
    $("#togglestop").click(function(){
        $("#stop_search").fadeToggle("fast");
    });
}
