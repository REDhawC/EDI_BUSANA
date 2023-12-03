// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://tradestat.commerce.gov.in/eidb/ecom.asp
// @icon         https://www.google.com/s2/favicons?sz=64&domain=gov.in
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    let table = document.getElementsByTagName("table")[0]
    let data = [];

    if (table) {

        // Get the table headers
        let headers = [];
        for (let j = 0, cell; cell = table.rows[0].cells[j]; j++) {
            headers.push(cell.innerText);
        }
        data.push(headers);

        for (let i = 1, row; row = table.rows[i]; i++) {
            let rowData = [];
            for (let j = 0, cell; cell = row.cells[j]; j++) {
                rowData.push(cell.innerText);
            }
            data.push(rowData);
        }

        let json = JSON.stringify(data);
        let blob = new Blob([json], { type: "application/json" });
        let url = URL.createObjectURL(blob);

        let a = document.createElement('a');
        a.download = "data.json";
        a.href = url;
        a.click();
    }




})();