// kind of a bad idea to have these globals but oh well it's version 1
var map;
var marker;
var geocoder;
var infowindow;
var locationCoordinates;

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
    // ajax csrf setup
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
    });

    $('#manAddrForm').submit(function (e) {
        e.preventDefault();
        // when they submit the address, display it on the map
        $('#manAddr').modal('hide');  // manually hide the modal
        // now convert the address to a location on the map. let's hope the user put in a nicely written location
        turnAddressToCoord(geocoder, map, $('#address').val(), infowindow);
    });

    $('#addLocationForm').submit(function (e) {
        e.preventDefault();
        // get the latitude and longitude and join them in a string and set them in the hidden input so later it can be picked up easily
        $('input[name=coords]').val([marker.getPosition().lat().toFixed(5), marker.getPosition().lng().toFixed(5)].join(','));

        $.ajax({
            url: $(this).attr("action"),
            type: "POST",
            dataType: "json",
            data: $(this).serialize(),
            success: function (resp) {
                if (resp.code === 0){
                    // if all went according to plan, then redirect them to the url of the new place
                    window.location = resp.newUrl;
                } else {
                    console.log("resp code: " + resp.code + ", message: " + resp.message);
                }
            },
            error: function (err) {
                console.log("error adding location: " + err.message);
            }
        });

    });

});