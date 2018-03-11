$(document).ready(function(){
    $('input[name=currentUrl]').val(window.location.pathname); // so we can redirect back to the original page after logging in
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

    // handle the user signup
    $('#signupForm').submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: "/advisor/register/",
            type: "POST",
			dataType: "json",
            data: $(this).serialize(),
            success: function(resp) {
                if (resp.statusCode === 0){
                    // everything was ok, user is registered, redirect them to original page
                    window.location = resp.currentUrl;
                } else {
                    alert('login failed');
                    // TODO: alert the user here that their register failed
                }
            },
            error: function(resp) {
                console.log("error" + resp);
            }
        });
    });

    // handle the user login
    $('#loginForm').submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: "/advisor/login/",
            type: "POST",
            dataType: "json",
            data:$(this).serialize(),
            success: function(resp) {
                if (resp.statusCode === 0){
                    // everything was ok, user is logged in, redirect them to original page
                    window.location = resp.currentUrl;
                } else {
                    alert('login failed');
                    // TODO: alert the user here that their login failed
                }
            },
            error: function(resp) {
                console.log(resp);
            }
        });
    });
	
	
	// handle review
    $('#reviewForm').submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: "/advisor/write_review/",
            type: "POST",
            dataType: "json",
            data:$(this).serialize(),
            success: function(resp) {
                if (resp.statusCode === 0){
                    // everything was ok, review posted
                    window.location = resp.currentUrl;
                } else {
                    alert('submit failed');
                    // TODO: alert the user here that something went wrong
                }
            },
            error: function(resp) {
                console.log(resp);
            }
        });
    });
	
	// handle review
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
						// everything was ok, review posted
						$('#btn-visited').attr('data-state',"true");
						$('#btn-visited').removeClass('btn-success');
						$('#btn-visited').toggleClass('btn-danger');
						$('#btn-visited').html('Click me if you haven\'t!');
						$('#been-here-text').html("You said that you have visited this place");
						var num_visited = parseInt($('#num-visits').html()) + 1;
						$('#num-visits').html(num_visited.toString());
						//window.location = resp.currentUrl;
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
						// everything was ok, review posted
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
	
	// handle review
    $('.location-item').click(function (e) {
        e.preventDefault();
		var url = $(this).children("input#url").val();
		console.log(url);
        window.location.href = url;
    });
	
	
});