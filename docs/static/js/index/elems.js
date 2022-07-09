// IMPORT / EXPORT ////////////////////////////////////////////////////////////////

document.getElementById("import").addEventListener('change', function(){
	let json = this.files[0];
	if(this.files[0] != null){
		let formData = new FormData();
		formData.append("file", json, json.name);

		document.getElementById("import").value  = null;
		showToast("Non disponibile nella versione di test.");
	}
});


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

	event.preventDefault();

	addData(title.value, season.value, [link.value], absolute.checked)
	.then(()=>{
		title.value = "";
		season.value = "";
		season.disabled = false;
		link.value = "";
		absolute.checked = false;
		this.closest(".modal").classList.remove("active");
	});

	
});
