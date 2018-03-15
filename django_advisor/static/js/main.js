$(document).ready(function () {
    $('input[name=currentUrl]').val(window.location.pathname); // so we can redirect back to the original page after logging in
    // ajax csrf setup
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
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
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            dataType: "json",
            data: $(this).serialize(),
            success: function (resp) {
                if (resp.statusCode === 0) {
                    // everything was ok, user is registered, redirect them to original page
                    swal({
                        type: 'success',
                        title: 'You have successfully register!',
                        text: 'Hold on while we take you to your profile...',
                        timer: 1500,
                        onOpen: function (e) {
                            swal.showLoading();
                        }
                    }).then(function (result) {
                        if (result.dismiss === swal.DismissReason.timer) {
                            window.location = '/advisor/profile/';
                        }
                    });
                } else {
                    swal({
                        type: 'error',
                        title: 'Error occured',
                        text: 'An error occured while trying to register you. Please try again later'
                    });
                }
            },
            error: function (resp) {
                console.log("error: " + resp);
            }
        });
    });

    // handle the user login
    $('#loginForm').submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            dataType: "json",
            data: $(this).serialize(),
            success: function (resp) {
                if (resp.statusCode === 0) {
                    // everything was ok, user is logged in, redirect them to original page
                    swal({
                        type: 'success',
                        title: 'Logging you in',
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
                        title: 'Error occured with login',
                        text: 'An error occured with login. Please try again later.'
                    })
                }
            },
            error: function (resp) {
                console.log(resp);
            }
        });
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

    // handle press on location tab in index page
    $('.location-item').click(function (e) {
        e.preventDefault();
        var url = $(this).children("input#url").val();
        console.log(url);
        window.location.href = url;
    });

    $('#search').keyup(function (e) {
        var searchFor = $(this).val();
        console.log(searchFor);
        $('#location-items-container').find('div.location-item').each(function () {
            var locationName = $(this).attr('name').toLowerCase();
            console.log(locationName + "     " + $(this).attr('name'));
            if (locationName.indexOf(searchFor) < 0) {
                this.style.display = "none";
            } else {
                this.style.display = "inline-block"
            }
        });
    });


});