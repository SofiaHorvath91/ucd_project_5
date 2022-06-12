/* Constant to pass jQuery for testing with Jest (book_quantity.test.js), to be commented out in Production */
//const $ = require('jquery');

$('.btt-link').click(function(e) {
    window.scrollTo(0,0)
})

$('#sort-selector').change(function() {
    var selector = $(this);
    var currentUrl = new URL(window.location);
    var selectedVal = selector.val();
    var newURL = setSearchValues(selectedVal, currentUrl);
    window.location.replace(newURL);
})

function setSearchValues(selectedVal, currentUrl){
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

        return currentUrl;
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");

        return currentUrl;
    }
}

/* Export modules for testing with Jest (books.test.js), to be commented out in Production */
//module.exports = { setSearchValues };