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
        $('div#location-items-container').find('div.location-item').each(function () {
			console.log($(this).attr('name'));
            var locationName = $(this).attr('data-location-name').toLowerCase();
            console.log(locationName + "     " + $(this).attr('name'));
            if (locationName.indexOf(searchFor) < 0) {
                this.style.display = "none";
            } else {
                this.style.display = "inline-block"
            }
        });
    });
});