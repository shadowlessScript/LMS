let children = document.querySelector(".news-container").children;
let newsContainer = document.querySelector(".news-container");
// let childCheck = children.childElementCount;
let mainContainerHeight = newsContainer.offsetHeight;
var totalwidth = 0
console.log(mainContainerHeight);
for (let i = 0; i < children.length; i++)
{
    totalwidth += parseInt(children[i].offsetHeight, 10);
}
let button = document.querySelector('.more')
if (mainContainerHeight < totalwidth)
{
    newsContainer.style.height = "65vh";
    button.style.display = "block";
}


button.addEventListener("click", () => {
    newsContainer.style.height = "auto";
    newsContainer.style.transition = "1s";
    button.style.display = "none";
});


    