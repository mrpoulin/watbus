var spinner;

function initialize() {
    var mapOptions = {options :{
		zoom: 16,
        maxZoom: 20,
        minZoom: 13,
		center: new google.maps.LatLng(43.47273, -80.541218),
		mapTypeId: google.maps.MapTypeId.ROADMAP
	}};

    // Defines the map. "gmap3" is the jQuery plugin for Google Maps
    $("#map-canvas").gmap3({
        map: mapOptions
    });

    // Add the spinner (stops when the marker is loaded)
    startSpinner();

    // Add event listener: wait for users to move the Viewport
    // Calls function showMarkers when the Viewport stops panning
    var map = $('#map-canvas').gmap3("get");
    google.maps.event.addListener(map, 'idle', showMarkers);

    // Attempt to get the user's location and center map around them
    getCustomLocation();
}

function showMarkers(){
    spinner.stop();
    startSpinner();
    var map = $('#map-canvas').gmap3("get");
    var bounds = map.getBounds();
    $.getJSON("/watbus/stopjson", function(data){
        addMarkers(data, bounds);
    });  
}

function getCustomLocation(){
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(function(pos){
            var latLng = new google.maps.LatLng(
                pos.coords.latitude, pos.coords.longitude);
            $("#map-canvas").gmap3("get").setCenter(latLng);
        });
    }
}

function inBounds(latLng, bounds){
    if(bounds.ea.b <= latLng[0] && latLng[0] <= bounds.ea.d){
        if(bounds.ia.b <= latLng[1] && latLng[1] <= bounds.ia.d){
            return true;
        }
    } 
    return false;
}

// Fetch stops within and add them to the map
function addMarkers(data, bounds){

    $('#map-canvas').gmap3('clear', 'marker');

    var markerArray = [];
    var latLngArray;
    var marker;

    $.each(data, function(key, stop){

        // Create objects like below, and put them in the array
        // {latLng: [48.8620722, 2.352047]}
        latLngArray = [stop.fields.stop_lat, stop.fields.stop_lon];
        if(inBounds(latLngArray, bounds)){
            marker = {
                latLng: latLngArray,
                events: {
                    click: function(marker, event, context){
                        // The JSON serializes stop_id as stop.pk
                        var newPage = "../browse/stops/" + stop.pk;
                        document.location.href = newPage;
                    }
                }

            };
            markerArray.push(marker);
        }
    });

    // Insert array of stops into map
    $("#map-canvas").gmap3({
        marker:{
            values: markerArray,
        }
    });
    spinner.stop();
}

function startSpinner(){
    var opts = {
        lines: 11, // The number of lines to draw
        length: 8, // The length of each line
        width: 5, // The line thickness
        radius: 12, // The radius of the inner circle
        corners: 1, // Corner roundness (0..1)
        rotate: 0, // The rotation offset
        direction: 1, // 1: clockwise, -1: counterclockwise
        color: '#000', // #rgb or #rrggbb or array of colors
        speed: 1, // Rounds per second
        trail: 60, // Afterglow percentage
        shadow: false, // Whether to render a shadow
        hwaccel: false, // Whether to use hardware acceleration
        className: 'spinner', // The CSS class to assign to the spinner
        zIndex: 2e9, // The z-index (defaults to 2000000000)
        top: 'auto', // Top position relative to parent in px
        left: 'auto' // Left position relative to parent in px
    };
    var target = document.getElementById('map-canvas');
    spinner = new Spinner(opts).spin(target);
}

$(document).ready(initialize);
