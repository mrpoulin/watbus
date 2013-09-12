function getUserLocation(){
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        var content = document.getElementById('content');
        content.append("Geolocation is not spported by this browser.");
    }
}

function showPosition(position){
    // You can access the user's longitude and latitude with the following:
    // position.coords.latitude
    // position.coords.longitude
}

var initialize = function(){
    var mapOptions = {options :{
		zoom: 15,
		center: new google.maps.LatLng(43.47273, -80.541218),
		mapTypeId: google.maps.MapTypeId.ROADMAP
	}};

    // Defines the map. "gmap3" is the jQuery plugin for Google Maps
    $("#map-canvas").gmap3({
        map: mapOptions,
    });

    getUserLocation();
}

function addMarkers(data){
    // Fetch stops and add them to the map
    var markerArray = [];
    var latLngArray;
    var marker;
    $.each(data, function(key, stop){
        // Create objects like below, and put them in the array
        // {latLng: [48.8620722, 2.352047]}
        latLngArray = [stop.fields.stop_lat, stop.fields.stop_lon];
        marker = {latLng: latLngArray};
        markerArray.push(marker);
    });
    // Insert array of stops into map
    $("#map-canvas").gmap3({
        marker:{
            values: markerArray
        }
    });
}

$(document).ready(initialize);
