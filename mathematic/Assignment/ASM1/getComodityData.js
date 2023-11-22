// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://tradestat.commerce.gov.in/eidb/ecomq.asp
// @icon         https://www.google.com/s2/favicons?sz=64&domain=gov.in
// @grant        none
// ==/UserScript==


// 1. get all the HS code
(function () {
    'use strict';

    let form = document.getElementsByName("form1")[0]
    let select = document.getElementById("select2")
    let digitSelect = document.getElementById("select1")
    let HSinput = document.getElementsByName("hscode")[0]
    let tickQuantity = document.getElementsByName("radioqty")[0]
    let tickValue = document.getElementsByName("radioval")[0]

    let arr_year = ["7", "9", '11']
    let arr_cropType = ["100610", "10061000", "10061010", "10061090", "100620", "10062000", "100630", "10063001", "10063002", "10063009", "10063010", "10063020", "10063090", "100640", "10064000"]


    for (let index = 0; index < arr_year.length; index++) {
        for (let index2 = 0; index2 < arr_cropType.length; index2++) {
            tickQuantity.checked = true
            tickValue.checked = false
            select.selectedIndex = arr_year[index]
            HSinput.value = arr_cropType[index2]
            if (arr_cropType[index2].length === 6) {
                digitSelect.selectedIndex = '2'
                form.target = "_blank";
                form.submit()
            }
            else if (arr_cropType[index2].length === 8) {
                digitSelect.selectedIndex = '3'
                form.target = "_blank";
                form.submit()
            }
            else {
                continue
            }
        }

    }
})();

