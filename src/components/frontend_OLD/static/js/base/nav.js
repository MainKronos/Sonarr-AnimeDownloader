// NAV //////////////////////////

document.querySelector("#nav.btn").addEventListener('click', function(){
	document.querySelector("nav").classList.add('active');
});

document.querySelector(".nav-overlay").addEventListener('click', function(){
	document.querySelector("nav").classList.remove('active');
});

document.querySelector('#rescan').addEventListener('click', function (e) {
	e.preventDefault();
	fetch("/api/rescan").then(res => res.json()).then(res => {
      showToast(res.data);
    }, error => {
      showToast(error)
    });
});



// TOAST //////////////////////////////////////////////////////

function showToast(message){
	let toast = document.createElement('div');
	toast.id = 'toast';

	time = 2000;

	toast.appendChild(document.createTextNode(message));
	document.body.appendChild(toast);

	setTimeout(function(){
		toast.classList.add("active");
		setTimeout(function(){
			toast.classList.remove("active");
			setTimeout(function(){
				document.body.removeChild(toast);
			}, time+500);
		},time);
	}, 500);
}

// MENU //////

class Menu{
	constructor(){
		this.menu = document.getElementById('menu');

		document.addEventListener('click', (e)=>this.hide(e));
		// document.addEventListener('contextmenu', (e)=>this.show(e));
	}

	#removeLabels(){
		while(this.menu.firstChild) this.menu.removeChild(this.menu.firstChild);
	}

	hide(event){
		this.menu.style.display = "none";
		this.menu.style.top = "";
		this.menu.style.left = "";

		this.#removeLabels();
	}

	show(event, labels=["Edit", "Delete"], events=[]){
		event.preventDefault();

		if(this.menu.style.display == "block") this.#removeLabels();

		this.menu.style.display = "block";
		this.menu.style.top = `${event.pageY}px`;
		this.menu.style.left = `${event.pageX}px`;

		labels.map((label, index)=>{
			let li = document.createElement('li');
			li.appendChild(document.createTextNode(label));
			this.menu.appendChild(li);
			li.addEventListener('click', events[index]);
		})
	}
}

const menu = new Menu();
