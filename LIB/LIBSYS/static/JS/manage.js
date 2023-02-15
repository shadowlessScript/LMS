let deleteBtn = document.querySelectorAll('[id=delete-btn]');
let deleteMsg = document.querySelectorAll('[class=confirm-msg]');
let counter = 0


for(var i = 0;i <= deleteBtn.length -1; i++){
	deleteBtn[i].addEventListener('click', ()=>{
	 counter++;
    console.log(counter);
    for(var j = 0; j <= deleteMsg.length - 1; j++){
	    if (counter % 2 === 1)
	    {    
	    	   
	        	deleteMsg[j].style.display = 'block';
	    	
	    } else
	    {
	    	   
	        	deleteMsg[j].style.display = 'none';
	    	
	    }
	}
})
}

// deleteBtn.addEventListener('click', ()=>{
// 	 counter++;
//     console.log(counter);

//     if (counter % 2 === 1)
//     {        
//         deleteMsg.style.display = 'block';
//     } else
//     {
//     	deleteMsg.style.display = 'none';
//     }
	
// })

// var names = '';
// for(var i = 0; i < deleteBtn.length; i++) {
//     names += deleteBtn[i].name;
// }
// console.log(names);