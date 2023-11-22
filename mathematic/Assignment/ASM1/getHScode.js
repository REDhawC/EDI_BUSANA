// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://tradestat.commerce.gov.in/eidb/searchq.asp?fl=ecomq.asp
// @icon         https://www.google.com/s2/favicons?sz=64&domain=gov.in
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    let form = document.getElementsByName("form1")[0]
    let HSinput = document.getElementsByName("Code")[0]

    let arr_cropType = ['1006',]
    // let arr_cropTypeHScode = []
    // let arr_cropType = ['rice', 'wheat', 'cotton', 'maize', 'horsegram', 'jute', 'potato', 'soyabean']


    for (let index = 0; index < arr_cropType.length; index++) {
        // select.value = "2010-2011"
        HSinput.value = arr_cropType[index]
        form.target = "_blank";
        form.submit()
    }




})();