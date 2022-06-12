/* Constant to pass jQuery for testing with Jest (book_quantity.test.js), to be commented out in Production */
const $ = require('jquery');

let countrySelected = $('#id_basic_country').val();
if(!countrySelected) {
    $('#id_basic_country').css('color', 'rgb(170, 183, 196)');
};

$('#id_basic_country').change(function() {
    countrySelected = $(this).val();
    setCountryFieldColor(countrySelected);
});

function setCountryFieldColor(countrySelected){
    if(!countrySelected) {
        document.getElementById("id_basic_country").style.color = 'rgb(170, 183, 196)';
    } else {
        document.getElementById("id_basic_country").style.color = 'rgb(0, 0, 0)';
    }
}

/* Export modules for testing with Jest (profiles_country.test.js), to be commented out in Production */
//module.exports = { setCountryFieldColor };