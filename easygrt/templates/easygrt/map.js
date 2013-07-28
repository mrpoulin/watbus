
var ourCoords = {
	latitude: 43.489377399999995,
	longitude: -79.6871133
};

window.onload = getMyLocation;

function getMyLocation()
{
	if(navigator.geolocation) {	
        // If the navigator geolocation object exists, browser supports API
		// Pass in a handler function
		navigator.geolocation.getCurrentPosition(displayLocation, displayError);
	} else {
		alert("Oops, no geolocation support");
	}
}

function displayLocation(position)
{
	var latitude = position.coords.latitude;
	var longitude = position.coords.longitude;
	
	var div = document.getElementById("location");
	div.innerHTML = " You are at latitude " + latitude + " longitude " + longitude;
	div.innerHTML += " (with " + position.coords.accuracy + "m accuracy)";

	var km = computeDistance(position.coords, ourCoords);
	var distance = document.getElementById("distance");
	distance.innerHTML = "You are " + km + " km from Holly";

	showMap(position.coords);	
}

function showMap(coords)
{
	var mapOptions = {
	  center: new google.maps.LatLng(coords.latitude, coords.longitude),
	  zoom: 16,
	  mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	
	var map = new google.maps.Map(document.getElementById("map"), mapOptions);
		  
}

function displayError(error)
{
	var errorTypes = 
	{
		0: "Unknown error",
		1: "Permission denied by user",
		2: "Position is not available",
		3: "Request timed out"
	}
	
	var errorMessage = errorTypes[error.code];
	if (error.code == 0 || error.code == 2) {
		errorMessage = errorMessage + " " + error.message;	
		// 0 and 2 might have extra info
	}
	var div = document.getElementById("location");
	div.innerHTML = errorMessage;
}
