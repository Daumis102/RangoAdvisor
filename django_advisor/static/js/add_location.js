// kind of a bad idea to have these globals but oh well it's version 1
var map;
var marker;
var geocoder;
var infowindow;

function initMap() {
    geocoder = new google.maps.Geocoder();
    infowindow = new google.maps.InfoWindow;
    var latLng = new google.maps.LatLng(55.872555, -4.289680);
    var options = {
        zoom: 12,
        center: latLng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map-addl"), options);

    marker = new google.maps.Marker({
        position: latLng,
        map: map
    });

    // feature, not necessary
    // google.maps.event.addListener(marker, 'dragend', function(e){
    //     // when they are dragging the marker itself
    // });

    google.maps.event.addListener(map, 'click', function(e){
        // for when they physically click on the map
        showCityFromLatLng(geocoder, map, infowindow, e.latLng);
    });
}

// idea is to get the coordinates, convert them to a readable address/location, and show it on the screen
function showCityFromLatLng(geocoder, map, infowindow, latLng){
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

function turnAddressToCoord(geocoder, map, address, infowindow){
    geocoder.geocode({'address': address}, function (results, status) {
        if (status === 'OK'){
            map.setCenter(results[0].geometry.location);
            marker.setPosition(results[0].geometry.location);
            infowindow.setContent(results[0].formatted_address);
            infowindow.open(map, marker);
        } else{
            console.log("geocode failed: " + status);
        }
    })
}


$(document).ready(function() {
    $('#manAddrForm').submit(function (e) {
        e.preventDefault();
        // when they submit the address, display it on the map
        $('#manAddr').modal('hide');  // manually hide the modal
        // now convert the address to a location on the map. let's hope the user put in a nicely written location
        turnAddressToCoord(geocoder, map, $('#address').val(), infowindow);
    });


});