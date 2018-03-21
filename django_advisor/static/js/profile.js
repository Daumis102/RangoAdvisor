$(function () {
    $('#changePWForm').submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: $(this).attr("method"),
            dataType: "json",
            data: $(this).serialize(),
            success: function (e) {
                if (e.statusCode === 0) {
                    swal({
                        type: 'success',
                        title: 'Password change successful',
                        text: 'Your password has been successfully changed'
                    });
                } else {
                    swal({
                        type: 'error',
                        title: 'Password change failed',
                        text: 'It seems your password failed to change. Please try again later.'
                    });
                }
            },
            error: function (e) {
                console.log(e);
            }
        });
    });

    // trigger the file chooser to show up
    $('button[id=changePP]').click(function (e) {
        e.preventDefault();
        $('input[name=newAvatar]').trigger('click');
    });

    $('input[name=newAvatar]').on('change', function (e) {
        // get the new image and send it to the backend
        var file = $(this).prop('files')[0];
        var reader = new FileReader();

        reader.addEventListener("load", function (ev) {
            var data = new FormData($('#changePPForm').get(0));
            $.ajax({
                url: $('form[id=changePPForm]').attr('action'),
                type: $('form[id=changePPForm]').attr('method'),
                contentType: false,
                processData: false,
                data: data,
                success: function (resp) {
                    resp = JSON.parse(resp);
                    if (resp.statusCode === 0) {
                        swal({
                            type: 'success',
                            title: 'Avatar change successful',
                            text: 'You have successfully changed your profile picture. Reloading your profile page now...',
                            timer: 3000,
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
                            title: 'Avatar change failed',
                            text: 'Your attempt to change the avatar failed. Please try again later.'
                        });
                    }
                },
                error: function (err) {
                    console.log(err);
                }
            });
        });

        reader.readAsDataURL(file);
    });

    $('.pseudo_link').on('click', function (e) {
        window.location = $(".pseudo_url").attr("value");
    });

    $('#deleteAcc').click(function (e) {
        swal({
            title: 'Are you sure?',
            text: 'You will not be able to revert this!',
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Do it'
        }).then(function (result) {
            if (result.value) {
                // delete account
                $.ajax({
                    url: '/advisor/profile/deleteaccount/',
                    type: 'post',
                    success: function (resp) {
                        console.log(resp);
                        swal({
                            title: 'Account deletion successful',
                            text: 'You have deleted your account. Sorry to see you go :( Taking you to the homepage...',
                            type: 'info',
                            timer: 1500,
                            onOpen: function (e) {
                                swal.showLoading();
                            }
                        }).then(function (value) {
                            window.location = '/advisor/index/';
                        });
                    },
                    error: function (resp) {
                        console.log(resp);
                        swal({
                            title: 'An error occured',
                            text: 'We do not know what happened',
                            type: 'info'
                        });
                    }
                });
            } else {
                // do not delete account
                swal({
                    title: 'Account not deleted',
                    text: 'Your account has not been deleted.',
                    type: 'info'
                })
            }

        });
    });
});