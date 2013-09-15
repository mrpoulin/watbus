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
        maxZoom: 20,
        minZoom: 13,
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
        marker = {
            latLng: latLngArray,
        /*  // Allows option to change the marker icon
            options: {
                icon: "../../static/watbus/img/marker.png"
            },*/
            events: {
                click: function(marker, event, context){
                    // The JSON serializes stop_id as stop.pk
                    var newPage = "../browse/stops/" + stop.pk;
                    document.location.href = newPage;
                }
            }

        };
        markerArray.push(marker);
    });
    // Insert array of stops into map
    $("#map-canvas").gmap3({
        marker:{
            values: markerArray,
        /*  allows markers to be clustered
            cluster: {
                // Size of the cluster radius
                radius: 50,
                events: {
                    mouseover: function(cluster){
                        var item = $(cluster.main.getDOMElement());
                        item.css("border", "1px solid red");
                    }, 
                    mouseout: function(cluster){
                        var item = $(cluster.main.getDOMElement());
                        item.css("border", "0px");
                    }
                },
                0: {
                    content: "<div class='cluster cluster-1'>CLUSTER_COUNT</div>",
                    width: 53, 
                    height: 52
                },
                20: {
                    content: "<div class='cluster cluster-2'>CLUSTER_COUNT</div>",
                    width: 56,
                    height: 55
                },
                50: {
                    content: "<div class='cluster cluster-3'>CLUSTER_COUNT</div>",
                    width: 66,
                    height: 65
                }
            }*/
        }
    });
}

$(document).ready(initialize);
