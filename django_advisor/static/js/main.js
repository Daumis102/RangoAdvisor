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
                        title: 'You have successfully registered!',
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
});