/* Constant to pass jQuery for testing with Jest (books.test.js), to be commented out in Production */
//const $ = require('jquery');

/* jQuery */

/* Scroll to top of page upon clicking on up arrow at page bottom */
$('.btt-link').click(function(e) {
    window.scrollTo(0,0);
});

/* React on sorting criteria change
and set new sorting condition by altering URL */
$('#sort-selector').change(function() {
    var selector = $(this);
    var currentUrl = new URL(window.location);
    var selectedVal = selector.val();
    var newURL = setSearchValues(selectedVal, currentUrl);
    window.location.replace(newURL);
});

/* Javascript Functions */

/* Upon user interaction (chaning sort selector),
set current sorting conditions and return altered URL */
function setSearchValues(selectedVal, currentUrl){
    if(selectedVal != "reset"){
        var sort = selectedVal.split("_")[0];
        var direction = selectedVal.split("_")[1];

        if(direction == 'depository'){
                var dir = selectedVal.split("_")[3];
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
//module.exports = { $, setSearchValues };