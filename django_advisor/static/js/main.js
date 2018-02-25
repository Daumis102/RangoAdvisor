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
            data: $(this).serialize(),
            success: function(resp) {
                console.log(resp);
            },
            error: function(resp) {
                console.log(resp);
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
    })
});