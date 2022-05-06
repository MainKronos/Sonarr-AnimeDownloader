// range

function syncData(){

	return fetch("/api/settings")
	.then(res => res.json())
	.then((res) => {
		document.getElementById('RenameEp').checked = res.data.RenameEp;
		document.getElementById('MoveEp').checked = res.data.MoveEp;
		document.getElementById('AutoBind').checked = res.data.AutoBind;

		document.getElementById('ScanDelay').value = res.data.ScanDelay;
		document.querySelector("#ScanDelay + label").textContent = res.data.ScanDelay;

		for(let elem of document.querySelectorAll('input[name=LogLevel]')){
			elem.checked = elem.value == res.data.LogLevel;
		}


	});
}
syncData();

document.getElementById('ScanDelay').addEventListener('input', function(event){
	document.querySelector("#ScanDelay + label").textContent = this.value;
});

function updateSettings(data){
	return fetch('/api/settings', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			AutoBind: data.hasOwnProperty('AutoBind') ? data.AutoBind : null,
			LogLevel: data.hasOwnProperty('LogLevel') ? data.LogLevel : null,
			MoveEp: data.hasOwnProperty('MoveEp') ? data.MoveEp : null,
			RenameEp: data.hasOwnProperty('RenameEp') ? data.RenameEp : null,
			ScanDelay: data.hasOwnProperty('ScanDelay') ? data.ScanDelay : null
		})
	})
	.then(response => response.json())
	.then(data => {
		showToast(data.data);
	});
}
document.getElementById('ScanDelay').addEventListener('change', function(event){
	updateSettings({ScanDelay: parseInt(this.value)});
});
document.getElementById('RenameEp').addEventListener('change', function(event){
	updateSettings({RenameEp: this.checked});
});
document.getElementById('MoveEp').addEventListener('change', function(event){
	updateSettings({MoveEp: this.checked});
});
document.getElementById('AutoBind').addEventListener('change', function(event){
	updateSettings({AutoBind: this.checked});
});
for(let elem of document.querySelectorAll('input[name=LogLevel]')){
	elem.addEventListener('change', function(event){
		if(this.checked) updateSettings({LogLevel: this.value})
	});
}

document.getElementById("import").addEventListener('change', function(){
	let json = this.files[0];
	if(this.files[0] != null){
		let formData = new FormData();
		formData.append("file", json, json.name);
		fetch('/ie/settings', {method: "POST", body: formData})
		.then(response => response.json())
		.then((res)=>{
			syncData();
			document.getElementById("import").value  = null;
			showToast(res["error"] ? res["error"] : "Impostazioni caricate con successo.")
		})
	}
});