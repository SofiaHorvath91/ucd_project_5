/*
 * @jest-environment jsdom
 */
require('jest-fetch-mock').enableMocks()

/* Initialize jQuery */
const $ = require('jquery');

/* Modules exported from profiles_country.js */
const { setCountryFieldColor } = require("./profiles_country");

/* Set up test objects and test UI */
beforeAll(() => {
    document.body.innerHTML =
    "<select name='basic_country' id='id_basic_country' style='color: rgb(0, 0, 0);'>"
    + "<option id='default_value' value=''>Country</option>"
    + "<option id='other_value' value='FR'>France</option>"
    + "</select>";
});

describe("Test of setting color of Country field when country is not selected", () => {
    beforeAll(() => {
        document.getElementById('default_value').selected = true;
        var color = document.getElementById('id_basic_country').value;
        setCountryFieldColor(color);
    });

    test("Country field's CSS color equals is grey when country not selected", () => {
        expect(document.getElementById("id_basic_country").style.color).toEqual('rgb(170, 183, 196)');
    });
});

describe("Test of setting color of Country field when country is selected", () => {
    beforeAll(() => {
        document.getElementById('other_value').selected = true;
        var color = document.getElementById('id_basic_country').value;
        setCountryFieldColor(color);
    });

    test("Country field's CSS color equals is black when country selected", () => {
        expect(document.getElementById("id_basic_country").style.color).toEqual('rgb(0, 0, 0)');
    });
});
