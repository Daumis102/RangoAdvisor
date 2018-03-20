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
	
	// handle visited people
    $('#btn-visited').click(function (e) {
		var state = $(this).attr("data-state");
		if(state=="false"){
			// register user to location visitors
			$.ajax({
				url: $(this).attr("action"),
				type: "POST",
				dataType: "json",
				data:{'location_id': $(this).attr("data-location-id"),'state':state},
				success: function(resp) {
					if (resp.statusCode === 0){
						// successfully registered to visited people
						$('#btn-visited').attr('data-state',"true");
						$('#btn-visited').removeClass('btn-success');
						$('#btn-visited').toggleClass('btn-danger');
						$('#btn-visited').html('Click me if you haven\'t!');
						$('#been-here-text').html("You said that you have visited this place");
						var num_visited = parseInt($('#num-visits').html()) + 1;
						$('#num-visits').html(num_visited.toString());
						
					} else {
						alert('Something went wrong');
					}
				},
				error: function(resp) {
					console.log(resp);
				}
			});
	} else {
		// unregister user from location visitors
		$.ajax({
				url: $(this).attr("action"),
				type: "POST",
				dataType: "json",
				data:{'location_id': $(this).attr("data-location-id"),'state':state},
				success: function(resp) {
					if (resp.statusCode === 0){
						// successfully unregistered from visited people
						$('#btn-visited').attr('data-state',"false");
						$('#btn-visited').removeClass('btn-danger');
						$('#btn-visited').toggleClass('btn-success');
						$('#btn-visited').html('Click me if you have!');
						$('#been-here-text').html("You said that you haven't visited this place");
						var num_visited = parseInt($('#num-visits').html()) - 1;
						$('#num-visits').html(num_visited.toString());
					} else {
						alert('Something went wrong');
					}
				},
				error: function(resp) {
					console.log(resp);
				}
			});
	}
    });
	
	// handle press on location tab in index page
    $('.location-item').click(function (e) {
        e.preventDefault();
		var url = $(this).children("input#url").val();
		console.log(url);
        window.location.href = url;
    });
	
	$('#search').keyup( function(e) {
		var searchFor = $(this).val();
		console.log(searchFor);
		$('#location-items-container').find('div.location-item').each(function(){
			var locationName = $(this).attr('name').toLowerCase();
			console.log(locationName + "     " +  $(this).attr('name'));
			if(	locationName.indexOf(searchFor)<0){
				this.style.display = "none";
			}else{
				this.style.display = "inline-block"
			}
		});
	});
	
	// handle upload photo button (make clicking proper button invoke click on file select input)
    $('#photo-upload-button').click( function() {
		$('#photo-upload-input').click();
	});

	$('#photo-upload-input').change(function (e) {
		var self = this;
		var photo = this.files.item(0);
		var type = photo.type;
		// check if file is of correct type
		if(type.match('image.*')){
			// file is correct. upload
			
			swal({
				title: 'Uploading..!',
				text: 'This might take a few seconds',
				timer: 2000,
				onOpen: function (e) {
					swal.showLoading();
				}
			})
			.then((success) => {
				
					// get location to which we are uploading:
				var loc = $(self).attr("data-location-slug");
				var formData = new FormData();
				formData.append("photo", photo);
				formData.append("location", loc);
				
				$.ajax({
					url: $(self).attr('data-url'),
					type: "POST",
					dataType: "json",
					data:formData,
					contentType: false, 
					processData: false,
					success: function(resp) {
						if (resp.statusCode === 0){
							// everything was ok, photo was uploaded
							
							// now we can update carousel to include uploaded photo without reloading the page to make user exp better
							var num_pictures = $("div#photos ol.carousel-indicators").children().length;
							$('div#photos ol.carousel-indicators').append(`<li data-target="#photos" data-slide-to=${num_pictures}></li>`);
							$('div#photos div.carousel-inner').append(`
									<div class="item" id="uploaded_photo_item">
										<img id="uploaded_photo" src="${resp.url}">
									</div>`);

							swal({
								type: "success",
								title: "Upload complete",
								text: "You picture was added to the slideshow",
							});
					
						} else {
							swal({
								type: "error",
								title: "Upload failed",
								text: "Some error occured",
							});
						}
					},
					error: function(resp) {
						swal({
							type: "error",
							title: "Upload failed",
							text: "Some error occured",
						});
						console.log(resp);
					}
				});
	
			});
			
		}
		
	});
});
