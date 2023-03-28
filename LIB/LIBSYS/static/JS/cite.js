let cite_btn = document.querySelector('#cite-book');
let cite_container = document.querySelector(".cite-container");
let closebtn = document.querySelector(".close-icon");

cite_btn.addEventListener('click', () => {
    cite_container.style.visibility = 'visible';
});

cite_container.addEventListener('click', () => {
    cite_container.style.visibility = 'hidden';
});

closebtn.addEventListener('click', () => { 
    cite_container.style.visibility = 'hidden';
});