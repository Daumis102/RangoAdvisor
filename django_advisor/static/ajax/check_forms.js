$(document).ready(function(){
	
	$("#login_form").submit(function(event) {
		event.preventDefault();
		var form = $(this).closest("form");
		var username = document.getElementById("id_username").value;
		var password = document.getElementById("id_password").value;
		
		$.ajax({
			type: "POST",
			url: form.attr('validate-user-url'),
			data: {
				username: 'username',
				password: 'password',
			}
			dataType: 'json',
			success: function (data) {
				if(data.hasOwnProperty('is_valid')){
					if(!data.is_valid){
						alert("User not found.");
					}
				}
				else if(data.hasOwnProperty('is_active')){
					if(!data.is_active){
						alert("User disabled.");
					}
				}
			}
		});
	});
});