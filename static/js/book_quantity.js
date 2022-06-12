 /*
* Disable +/- buttons outside 1-99 range.
* If no size is passed to the function, the parameter will have a value of undefined by default,
* which prevents any errors
*/

/* Constant to pass jQuery for testing with Jest (book_quantity.test.js), to be commented out in Production */
//const $ = require('jquery');

/* jQuery */

// Ensure proper enabling/disabling of all inputs on page load
var allQtyInputs = $('.qty_input');
for(var i = 0; i < allQtyInputs.length; i++){
    var itemId = $(allQtyInputs[i]).data('item_id');
    handleEnableDisable(itemId);
}

// Check enable/disable every time the input is changed
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

/* Functions */

function handleEnableDisable(itemId) {
    var currentValue = parseInt($(`.id_qty_${itemId}`).val());

    var minusDisabled = currentValue < 2;
    var plusDisabled = currentValue > 98;

    $(`.decrement-qty_${itemId}`).prop('disabled', minusDisabled);
    $(`.increment-qty_${itemId}`).prop('disabled', plusDisabled);
}

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