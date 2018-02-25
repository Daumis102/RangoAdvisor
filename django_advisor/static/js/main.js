// function extendObj(obj1, obj2){
//     for (var key in obj2){
//         if(obj2.hasOwnProperty(key)){
//             obj1[key] = obj2[key];
//         }
//     }
//     return obj1;
// }
//
// $(document).ready(function(){
//     // ajax csrf setup
//     $.ajaxSetup({
//         headers: {
//             'X-CSRF-Token': $('meta[name="csrfmiddlewaretoken"]').attr('content')
//         }
//     });
//
//     // handle the user signup
//     $('#signupForm').submit(function (e) {
//         // var submitBtn = $(this).find('input[type=submit]');
//         // submitBtn.prop('disabled', true);
//
//         e.preventDefault();
//
//         $.ajax({
//             url: "/advisor/register/",
//             type: "POST",
//             data: $(this).serialize(),
//             success: function(resp) {
//                 console.log(JSON.parse(resp));
//             },
//             error: function(response) {
//                 console.log(JSON.parse(response));
//             }
//         });
//     });
//
//     // handle the user login
//     // $('#loginForm').submit(function (e) {
//     //     // var submitBtn = $(this).find('input[type=submit]');
//     //     // submitBtn.prop('disabled', true);
//     //
//     //     e.preventDefault();
//     //
//     //     $.ajax({
//     //         url: "/advisor/login/",
//     //         type: "POST",
//     //         dataType: "json",
//     //         data: {
//     //             csrfmiddlewaretoken: $('meta[name="csrfmiddlewaretoken"]').attr('content'),
//     //             loginUsername: document.getElementById("loginUsername").value,
//     //             loginPassword: document.getElementById("loginPassword").value
//     //         },
//     //         success: function(resp) {
//     //             console.log(JSON.parse(resp));
//     //         },
//     //         error: function(response) {
//     //             console.log(JSON.parse(response));
//     //         }
//     //     });
//     // })
// });