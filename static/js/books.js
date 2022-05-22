$('.btt-link').click(function(e) {
    window.scrollTo(0,0)
})

$('#sort-selector').change(function() {
    var selector = $(this);
    var currentUrl = new URL(window.location);

    var selectedVal = selector.val();
    if(selectedVal != "reset"){
        var sort = selectedVal.split("_")[0];
        var direction = selectedVal.split("_")[1];

        if(direction == 'depository'){
                dir = selectedVal.split("_")[3];
                currentUrl.searchParams.set("sort", 'book_depository_stars');
                currentUrl.searchParams.set("direction", dir);
        } else {
                currentUrl.searchParams.set("sort", sort);
                currentUrl.searchParams.set("direction", direction);
        }

        window.location.replace(currentUrl);
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");

        window.location.replace(currentUrl);
    }
})