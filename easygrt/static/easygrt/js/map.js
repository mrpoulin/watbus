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

}

$(document).ready(initialize);
