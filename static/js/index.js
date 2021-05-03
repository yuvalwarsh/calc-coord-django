$(document).ready(function() {

    $(".copyright").removeClass("in-jquery").text("Copyright © CalCoord " + new Date().getFullYear())


    $(document).on('change', ':file', function() {
        var input = $(this),
            label = input.val().replace(/\\/g, '/').replace(/.*\//, '');

        $(".filename").removeClass("in-jquery").text(label);
});

});

