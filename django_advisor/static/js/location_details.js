var map;
var marker;
var geocoder;
var infowindow;

function initMap() {
    geocoder = new google.maps.Geocoder();
    infowindow = new google.maps.InfoWindow;
    var latLng = new google.maps.LatLng(lat, lng);

    var options = {
        zoom: 12,
        center: latLng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map"), options);

    marker = new google.maps.Marker({
        position: latLng,
        map: map
    });
	
	// show more info about the place if available
	displayAddressFromLatLng(geocoder, map, infowindow, latLng);
	
}

// idea is to get the coordinates, convert them to a readable address/location, and show it on the screen
function displayAddressFromLatLng(geocoder, map, infowindow, latLng){
    geocoder.geocode({'location': latLng}, function(results, status){
        if (status === 'OK'){
            if (results[0]) {
                marker.setPosition(latLng);
                infowindow.setContent(results[0].formatted_address);
                infowindow.open(map, marker);

            } else{
                console.log("no results found");
            }
        } else{
            console.log("geocoder failed: " + status);
        }
    });
}
