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

    // Attempt to get the user's location and center map around them
    getCustomLocation();
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
    spinner.stop();
}

$(document).ready(initialize);
