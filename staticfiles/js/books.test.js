/*
 * @jest-environment jsdom
 */
require('jest-fetch-mock').enableMocks()

/* Initialize jQuery */
const $ = require('jquery');

/* Modules exported from book_quantity.js */
const { setSearchValues } = require("./books");

/* Set up test objects and test UI */
beforeAll(() => {
    document.body.innerHTML =
        "<select id='sort-selector'>"
        +"<option id='reset' value='reset'>Sort by...</option>"
        +"<option id='price_asc' value='price_asc'>Price (low to high)</option>"
        +"<option id='price_desc' value='price_desc'>Price (high to low)</option>"
        +"<option id='book_depository_stars_asc' value='book_depository_stars_asc'>Rating (low to high)</option>"
        +"<option id='book_depository_stars_desc' value='book_depository_stars_desc'>Rating (high to low)</option>"
        +"<option id='name_asc' value='name_asc'>Name (A-Z)</option>"
        +"<option id='name_desc' value='name_desc'>Name (Z-A)</option>"
        +"<option id='category_asc' value='category_asc'>Category (A-Z)</option>"
        +"<option id='category_desc' value='category_desc'>Category (Z-A)</option>"
        +"</select>";
});

/* Test function 'setSearchValues' to set search parameters for filtering books */

describe("Test of search among books with parameters Sort:Price / Direction:Asc ", () => {
    it('Test of returned URL with console log', () => {
        var selection = document.getElementById('price_asc');
        selection.selected = true;
        var currentUrl = new URL("https://example.com");
        var newURL = String(setSearchValues(selection.value, currentUrl));

        const consoleSpy = jest.spyOn(console, 'log');
        console.log(newURL);
        expect(consoleSpy).toHaveBeenCalledWith('https://example.com/?sort=price&direction=asc');
    });
});

describe("Test of search among books with parameters Sort:Price / Direction:Desc ", () => {
    it('Test of returned URL with console log', () => {
        var selection = document.getElementById('price_desc');
        selection.selected = true;
        var currentUrl = new URL("https://example.com");
        var newURL = String(setSearchValues(selection.value, currentUrl));

        const consoleSpy = jest.spyOn(console, 'log');
        console.log(newURL);
        expect(consoleSpy).toHaveBeenCalledWith('https://example.com/?sort=price&direction=desc');
    });
});

describe("Test of search among books with parameters Sort:Book Depo Price / Direction:Asc ", () => {
    it('Test of returned URL with console log', () => {
        var selection = document.getElementById('book_depository_stars_asc');
        selection.selected = true;
        var currentUrl = new URL("https://example.com");
        var newURL = String(setSearchValues(selection.value, currentUrl));

        const consoleSpy = jest.spyOn(console, 'log');
        console.log(newURL);
        expect(consoleSpy).toHaveBeenCalledWith('https://example.com/?sort=book_depository_stars&direction=asc');
    });
});

describe("Test of search among books with parameters Sort:Book Depo Price / Direction:Desc ", () => {
    it('Test of returned URL with console log', () => {
        var selection = document.getElementById('book_depository_stars_desc');
        selection.selected = true;
        var currentUrl = new URL("https://example.com");
        var newURL = String(setSearchValues(selection.value, currentUrl));

        const consoleSpy = jest.spyOn(console, 'log');
        console.log(newURL);
        expect(consoleSpy).toHaveBeenCalledWith('https://example.com/?sort=book_depository_stars&direction=desc');
    });
});

describe("Test of search among books with parameters Sort:Name / Direction:Asc ", () => {
    it('Test of returned URL with console log', () => {
        var selection = document.getElementById('name_asc');
        selection.selected = true;
        var currentUrl = new URL("https://example.com");
        var newURL = String(setSearchValues(selection.value, currentUrl));

        const consoleSpy = jest.spyOn(console, 'log');
        console.log(newURL);
        expect(consoleSpy).toHaveBeenCalledWith('https://example.com/?sort=name&direction=asc');
    });
});

describe("Test of search among books with parameters Sort:Name / Direction:Desc ", () => {
    it('Test of returned URL with console log', () => {
        var selection = document.getElementById('name_desc');
        selection.selected = true;
        var currentUrl = new URL("https://example.com");
        var newURL = String(setSearchValues(selection.value, currentUrl));

        const consoleSpy = jest.spyOn(console, 'log');
        console.log(newURL);
        expect(consoleSpy).toHaveBeenCalledWith('https://example.com/?sort=name&direction=desc');
    });
});

describe("Test of search among books with parameters Sort:Category / Direction:Asc ", () => {
    it('Test of returned URL with console log', () => {
        var selection = document.getElementById('category_asc');
        selection.selected = true;
        var currentUrl = new URL("https://example.com");
        var newURL = String(setSearchValues(selection.value, currentUrl));

        const consoleSpy = jest.spyOn(console, 'log');
        console.log(newURL);
        expect(consoleSpy).toHaveBeenCalledWith('https://example.com/?sort=category&direction=asc');
    });
});

describe("Test of search among books with parameters Sort:Category / Direction:Desc ", () => {
    it('Test of returned URL with console log', () => {
        var selection = document.getElementById('category_desc');
        selection.selected = true;
        var currentUrl = new URL("https://example.com");
        var newURL = String(setSearchValues(selection.value, currentUrl));

        const consoleSpy = jest.spyOn(console, 'log');
        console.log(newURL);
        expect(consoleSpy).toHaveBeenCalledWith('https://example.com/?sort=category&direction=desc');
    });
});