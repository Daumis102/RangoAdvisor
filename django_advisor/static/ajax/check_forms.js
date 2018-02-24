$(document).ready(function(){
	
	$("#form-signin").submit(function(event) {
		event.preventDefault();
		alert("submit");
		
		var username = document.getElementById("id_username").value;
		var password = document.getElementById("id_password").value;
		alert(username + " " + password);
		$.ajax({
			url: form.attr('validate-user-url'),
			data: form.serialize(),
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