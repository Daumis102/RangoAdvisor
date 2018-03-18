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
function displayAddressFromLatLng(geocoder, map, infowindow, latLng) {
    geocoder.geocode({'location': latLng}, function (results, status) {
        if (status === 'OK') {
            if (results[0]) {
                marker.setPosition(latLng);
                infowindow.setContent(results[0].formatted_address);
                infowindow.open(map, marker);

            } else {
                console.log("no results found");
            }
        } else {
            console.log("geocoder failed: " + status);
        }
    });
}

$(function () {
    $btn_visited = $('#btn-visited');
    $num_visits = $('#num-visits');
    // handle visited people
    $btn_visited.click(function (e) {
        var state = $(this).attr("data-state");
        if (state == "false") {
            // register user to location visitors
            $.ajax({
                url: $(this).attr("action"),
                type: "POST",
                dataType: "json",
                data: {'location_id': $(this).attr("data-location-id"), 'state': state},
                success: function (resp) {
                    if (resp.statusCode === 0) {
                        // successfully registered to visited people
                        $btn_visited.attr('data-state', "true");
                        $btn_visited.removeClass('btn-success');
                        $btn_visited.toggleClass('btn-danger');
                        $btn_visited.html('Click me if you haven\'t!');
                        $('#been-here-text').html("You said that you have visited this place");
                        var num_visited = parseInt($num_visits.html()) + 1;
                        $num_visits.html(num_visited.toString());

                    } else {
                        alert('Something went wrong');
                    }
                },
                error: function (resp) {
                    console.log(resp);
                }
            });
        } else {
            // unregister user from location visitors
            $.ajax({
                url: $(this).attr("action"),
                type: "POST",
                dataType: "json",
                data: {'location_id': $(this).attr("data-location-id"), 'state': state},
                success: function (resp) {
                    if (resp.statusCode === 0) {
                        // successfully unregistered from visited people
                        $btn_visited.attr('data-state', "false");
                        $btn_visited.removeClass('btn-danger');
                        $btn_visited.toggleClass('btn-success');
                        $btn_visited.html('Click me if you have!');
                        $('#been-here-text').html("You said that you haven't visited this place");
                        var num_visited = parseInt($num_visits.html()) - 1;
                        $num_visits.html(num_visited.toString());
                    } else {
                        alert('Something went wrong');
                    }
                },
                error: function (resp) {
                    console.log(resp);
                }
            });
        }
    });

    // handle review
    $('#reviewForm').submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            dataType: "json",
            data: $(this).serialize(),
            success: function (resp) {
                if (resp.statusCode === 0) {
                    // everything was ok, review posted
                    swal({
                        type: 'success',
                        title: 'Review posted!',
                        text: 'Reloading page...',
                        timer: 1500,
                        onOpen: function (e) {
                            swal.showLoading();
                        }
                    }).then(function (result) {
                        if (result.dismiss === swal.DismissReason.timer) {
                            window.location = resp.currentUrl;
                        }
                    });
                } else {
                    swal({
                        type: 'error',
                        title: 'An error occured',
                        text: 'An error occured trying to post your review. Please try again later'
                    });
                }
            },
            error: function (resp) {
                console.log(resp);
            }
        });
    });

});
