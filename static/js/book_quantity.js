/* Constant to pass jQuery for testing with Jest (book_quantity.test.js), to be commented out in Production */
//const $ = require('jquery');

/* jQuery */

// Ensure proper enabling/disabling of increase/decrease of quantity inputs on page load
var allQtyInputs = $('.qty_input');
for(var i = 0; i < allQtyInputs.length; i++){
    var itemId = $(allQtyInputs[i]).data('item_id');
    handleEnableDisable(itemId);
}

// Enable/disable increase/decrease of quantity inputs every time the input is changed
$('.qty_input').change(function() {
    var itemId = $(this).data('item_id');
    handleEnableDisable(itemId);
});

// Increment quantity
$('.increment-qty').click(function(e) {
   e.preventDefault();
   var itemId = $(this).data('item_id');
   var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
   var allQuantityInputs = $(`.input-group-${itemId} input[name='quantity']`);
   setQuantityInput($, allQuantityInputs[0].id, closestInput, 'plus');
   handleEnableDisable(itemId);
});

// Decrement quantity
$('.decrement-qty').click(function(e) {
   e.preventDefault();
   var itemId = $(this).data('item_id');
   var closestInput = $(this).closest('.input-group').find('.qty_input')[0];
   var allQuantityInputs = $(`.input-group-${itemId} input[name='quantity']`);
   setQuantityInput($, allQuantityInputs[0].id, closestInput, 'minus');
   handleEnableDisable(itemId);
});

/* Javascript Functions */

/* Handle enablement/disablement of quantity increase/decrease option
if quantity is on the edge of min-max range (1-99) */
function handleEnableDisable(itemId) {
    var currentValue = parseInt($(`.id_qty_${itemId}`).val());

    var minusDisabled = currentValue < 2;
    var plusDisabled = currentValue > 98;

    $(`.decrement-qty_${itemId}`).prop('disabled', minusDisabled);
    $(`.increment-qty_${itemId}`).prop('disabled', plusDisabled);
}

/* Display new quantity input on UI upon user interaction */
function setQuantityInput($, allQuantityInputs, closestInput, ops){
    var currentValue = parseInt($(closestInput).val());
    if(ops == 'minus'){
        document.getElementById(allQuantityInputs).value = currentValue - 1;
    } else{
         document.getElementById(allQuantityInputs).value = currentValue + 1;
    }
}

/* Export modules for testing with Jest (book_quantity.test.js), to be commented out in Production */
//module.exports = { allQtyInputs, handleEnableDisable, setQuantityInput };