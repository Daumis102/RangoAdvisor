// i stand by my globals
var map;
var marker;
var geocoder;
var infowindow;
var city = "Glasgow"; // default Glasgow because that's where the map marker is by default. bad idea but it works

function initMap() {
    geocoder = new google.maps.Geocoder(); // init the geocoder
    infowindow = new google.maps.InfoWindow; // init the infowindow
    var latLng = new google.maps.LatLng(55.872555, -4.289680); // set the default maps markers
    var options = { // set the options for the map
        zoom: 12,
        center: latLng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map-addl"), options); // init map on the page

    marker = new google.maps.Marker({ // create a new marker on the map
        position: latLng,
        map: map
    });

    google.maps.event.addListener(map, 'click', function(e){ // add event listener to whenever the user clicks on the map anywhere
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
                city = results[0].address_components[2].long_name;
                infowindow.open(map, marker);
            } else{
                console.log("no results found");
            }
        } else{
            console.log("geocoder failed: " + status);
        }
    });
}

// this is for when the user enters a human readable address. it will convert it to coordinates and display them on map
function turnAddressToCoord(geocoder, map, address, infowindow){
    geocoder.geocode({'address': address}, function (results, status) {
        if (status === 'OK'){
            map.setCenter(results[0].geometry.location);
            marker.setPosition(results[0].geometry.location);
            infowindow.setContent(results[0].formatted_address);
            city = results[0].address_components[2].long_name;
            infowindow.open(map, marker);
        } else{
            console.log("geocode failed: " + status);
            swal({
                type: 'error',
                title: 'Address not found',
                text: 'The address could not be found. Please try again'
            });
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

    $('#addLocationForm').submit(function (e) {
        e.preventDefault();
        // get the latitude and longitude and join them in a string and set them in the hidden input so later it can be picked up easily
        $('input[name=coords]').val([marker.getPosition().lat().toFixed(5), marker.getPosition().lng().toFixed(5)].join(','));
        $('input[name=city]').val(city);
        var data = new FormData($('#addLocationForm').get(0));
        $.ajax({
            url: $(this).attr("action"),
            type: $(this).attr("method"),
            data: data,
            contentType: false,
            processData: false,
            success: function (resp) {
                resp = JSON.parse(resp);
                if (resp.statusCode === 0){
                    // if all went according to plan, then redirect them to the url of the new place
                    swal({
                        type: 'success',
                        title: 'New location added!',
                        text: 'Your location has been added! Taking you to it now...',
                        timer: 3000,
                        onOpen: function (e) {
                            swal.showLoading();
                        }
                    }).then(function (result) {
                        if (result.dismiss === swal.DismissReason.timer){
                            window.location = resp.message;
                        }
                    });
                } else {
                    swal({
                        type: 'error',
                        title: 'An error occured',
                        text: 'An error with the addition of your new location. Please try again later'
                    });
                }
            },
            error: function (err) {
                err = JSON.parse(err);
                console.log("error adding location: " + err.message);
            }
        });
    });

    // make the image appear in the carousel when they upload one
    $('input[name=location_image]').on('change', function (e) {
        var file = $(this).prop('files')[0];
        var reader = new FileReader();

        reader.addEventListener("load", function (e) {
            var picture = e.target;
            $('img[id=ci]').attr("src", picture.result); // set the picture in the carousel
        });

        reader.readAsDataURL(file); // read the picture
    });

});