// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://tradestat.commerce.gov.in/eidb/search.asp?fl=ecomq.asp
// @icon         https://www.google.com/s2/favicons?sz=64&domain=gov.in
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    let table = document.getElementsByTagName("table")[0]
    let data = [];
    for (let i = 1, row; row = table.rows[i]; i++) {
        data.push(row.cells[0].innerText);
    }

    let json = JSON.stringify(data);
    let blob = new Blob([json], { type: "application/json" });
    let url = URL.createObjectURL(blob);

    let a = document.createElement('a');
    a.download = "data.json";
    a.href = url;
    a.click();

    alert("done")


})();