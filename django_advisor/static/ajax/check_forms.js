$(document).ready(function(){
	
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
	
	
	
	$("#login_form").submit(function(event) {
		event.preventDefault();
		var form = $(this).closest("form");
		var username = document.getElementById("id_username").value;
		var password = document.getElementById("id_password").value;
		var csrftoken = getCookie('csrftoken');
		
		function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			}
		});
		
		
		$.ajax({
			type: "POST",
			url: form.attr('validate-user-url'),
			data: {
				username: 'username',
				password: 'password',
			},
			dataType: 'json',
			success: function (data) {
				if(data.hasOwnProperty('is_valid')){
					if(!data.is_valid){
						alert("User not found. " + data.is_valid);
					}
				}
				else if(data.hasOwnProperty('is_active')){
					if(data.is_active == "false"){
						alert("User disabled.");
					}
				}
			}
		});
	});
	
	
	$("#register_form").submit(function(event) {
		event.preventDefault();
		var form = $(this).closest("form");
		var username = document.getElementById("id_username").value;
		var password = document.getElementById("id_password").value;
		var csrftoken = getCookie('csrftoken');
		
		function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			}
		});
		
		
		$.ajax({
			type: "POST",
			url: form.attr('register-user-url'),
			data: form.serialize(),
			},
			dataType: 'json',
			success: function (data) {
				if(data.hasOwnProperty('username_taken')){
					if(data.username_taken){
						alert("Username is already taken");
					}
				}
				if(data.hasOwnProperty('error')){
					if(data.error){
						alert("Error has occured");
					}
				}
			}
		});
	});
	
});