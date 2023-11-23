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
    // let arr_cropType = ["100610", "10061000", "10061010", "10061090", "100620", "10062000", "100630", "10063001", "10063002", "10063009", "10063010", "10063020", "10063090", "100640", "10064000"]
    // let arr_cropType = ["1001", "100110", "10011000", "10011010", "10011090", "100111", "10011100", "100119", "10011900", "100190", "10019001", "10019002", "10019003", "10019010", "10019020", "10019031", "10019039", "100191", "10019100", "100199", "10019910", "10019920"]
    // let arr_cropType = ["5201", "520100", "52010001", "52010011", "52010012", "52010013", "52010014", "52010015", "52010019", "52010020", "52010021", "52010022", "52010023", "52010024", "52010025"]
    // let arr_cropType =["1005","100510","10051000","100590","10059000","10059011","10059019","10059020","10059030","10059090"]
    // let arr_cropType =["0713","071310","07131000","07131010","07131020","07131090","071320","07132000","07132010","07132020","07132090","071331","07133100","07133110","07133190","071332","07133200","071333","07133300","071334","07133400","071335","07133500","071339","07133900","07133901","07133909","07133910","07133990","071340","07134000","071350","07135000","071360","07136000","071390","07139001","07139002","07139003","07139004","07139005","07139009","07139010","07139090","07139091","07139099"]
    // let arr_cropType =["5303","530310","53031001","53031002","53031003","53031009","53031010","53031090","530390","53039001","53039009","53039010","53039090"]
    let arr_cropType =["0701","070110","07011000","070190","07019000"]
    // let arr_cropType =["1201","120100","12010000","12010010","12010090","120110","12011000","120190","12019000"]

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

