$(function () {
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