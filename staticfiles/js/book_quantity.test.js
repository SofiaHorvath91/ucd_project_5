/*
 * @jest-environment jsdom
 */
require('jest-fetch-mock').enableMocks()

/* Initialize jQuery */
const $ = require('jquery');

/* Modules exported from book_quantity.js */
const { allQtyInputs,
        handleEnableDisable,
        setQuantityInput } = require("./book_quantity");

/* Set up test objects and test UI */
beforeAll(() => {
    document.body.innerHTML =
    "<div class='input-group input-group-1'><button class='decrement-qty decrement-qty_1' data-item_id='1' id='decrement-qty_1'></button>"
    + "<input class='qty_input id_qty_1' type='number' name='quantity' min='1' max='99' data-item_id='1' id='id_qty_1'>"
    + "<button class='increment-qty increment-qty_1' data-item_id='1' id='increment-qty_1'></button></div>";
});

/* Test function 'handleEnableDisable' with maximum quantity (disable of adding more) */
describe("Test of trying to add more books to basket than maximum allowed quantity (99)", () => {
    beforeAll(() => {
        document.getElementById("id_qty_1").value = 99
        handleEnableDisable(1);
    });

    test("Disabling option of adding more books", () => {
        expect(document.getElementById("increment-qty_1").disabled).toEqual(true);
    });
});

/* Test function 'handleEnableDisable' with minimum quantity (disable of removing more) */
describe("Test of trying to remove less books from basket than minimum allowed quantity (1)", () => {
    beforeAll(() => {
        document.getElementById("id_qty_1").value = 1
        handleEnableDisable(1);
    });

    test("Disabling option of adding more books", () => {
        expect(document.getElementById("decrement-qty_1").disabled).toEqual(true);
    });
});

/* Test jQuery event of 'setQuantityInput' */
describe( 'Set value of current quantity of books based on user input', () => {
	const val = jest.fn();
	const jQuery = jest.fn(() => ({
        val,
	}));

	it( 'Retrieving current quantity value and setting new quantity value with jQuery', () => {
        setQuantityInput(jQuery, 'id_qty_1', 'id_qty_1', 'plus');
        expect(val.mock.calls.length).toBe(1);
	});

	it( 'Increasing quantity value and setting new quantity value with jQuery', () => {
        $("#id_qty_1").val(3);
        let e = $.Event("click");
        $("#increment-qty_1").trigger(e);

        expect($("#id_qty_1").val()).toEqual("3");
	});

    it( 'Decreasing quantity value and setting new quantity value with jQuery', () => {
        $("#id_qty_1").val(2);
        let e = $.Event("click");
        $("#decrement-qty_1").trigger(e);

        expect($("#id_qty_1").val()).toEqual("2");
	});
});