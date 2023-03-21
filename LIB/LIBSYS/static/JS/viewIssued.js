"use strict";

let btn = document.querySelector('.btn');
let txt = document.querySelector('.stepping-stone')
let btn1 = document.querySelector('.close')
let counter = 0
btn.addEventListener('click', () => {

        txt.style.display = 'block';
        txt.style.transition = '1s';

});

btn1.addEventListener('click', () => {

     txt.style.display = 'none';

});