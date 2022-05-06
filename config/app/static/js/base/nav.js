
// NAV //////////////////////////

document.querySelector("#nav.btn").addEventListener('click', function(){
	document.querySelector("nav").classList.add('active');
});

document.querySelector(".nav-overlay").addEventListener('click', function(){
	document.querySelector("nav").classList.remove('active');
});



// TOAST //////////////////////////////////////////////////////

function showToast(message){
	let toast = document.createElement('div');
	toast.id = 'toast';

	toast.appendChild(document.createTextNode(message));
	document.body.appendChild(toast);

	setTimeout(function(){
		toast.classList.add("active");
		setTimeout(function(){
			toast.classList.remove("active");
			setTimeout(function(){
				document.body.removeChild(toast);
			}, 500);
		},3000);
	}, 500);
}
