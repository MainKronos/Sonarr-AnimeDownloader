// MODAL ////////////////////////////////////////////////////////////////

document.querySelector('#add-anime').addEventListener('click', function(){
	let modal = document.querySelector('#add-anime-modal');
	modal.classList.add("active");
});

document.querySelector('.modal-overlay').addEventListener('click', function(event){
	this.closest(".modal").classList.remove("active");
});

document.getElementById("absolute").addEventListener('change', function(event){
	document.getElementById('season').disabled = this.checked;
});

document.querySelector('form.modal-content').addEventListener('submit', function(event){
	let title = this.querySelector('#title');
	let season = this.querySelector('#season');
	let absolute = this.querySelector('#absolute');
	let link = this.querySelector('#link');

	addData(title.value, season.value, [link.value], absolute.checked)
	.then(()=>{
		title.value = "";
		season.value = "";
		season.disabled = false;
		link.value = "";
		absolute.checked = false;
		this.closest(".modal").classList.remove("active");
	});

	event.preventDefault();
});

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
