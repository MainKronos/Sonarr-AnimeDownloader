// per le informazione nella pagina log.html

inter = 0
setInterval(() => {
	max_time = 900
	inter = inter%max_time;


	data = {
		filename: "Call of the Night - S1E1",
		percentage: inter/max_time,
		downloaded_bytes: 260.380*inter,
		total_bytes: 234342147,
		elapsed: inter,
		eta: max_time - inter,
		speed: 260380
	}

	document.getElementById('download-info').classList.add("active");

	let filename = document.querySelector("#filename");
	let percentage = document.querySelector("div.progress > label#percentage");
	let percentage_bar = document.querySelector("div.progress > span");
	let downloaded = document.querySelector("#downloaded");
	let elapsed = document.querySelector("#elapsed");
	let speed = document.querySelector("#speed");
	let eta = document.querySelector("#eta");


	filename.textContent = data.filename;
	percentage.textContent = `${Math.round(data.percentage * 1000)/10}%`;
	percentage_bar.style.width = `${data.percentage * 100}%`;
	downloaded.textContent = `${unitConversion(data.downloaded_bytes)} / ${unitConversion(data.total_bytes)}`;
	
	elapsed.textContent = new Date(data.elapsed * 1000).toISOString().slice(11,-5);
	eta.textContent = new Date(data.eta * 1000).toISOString().slice(11,-5);
	speed.textContent = unitConversion(Math.round(data.speed)) + '/s';

	if(data.percentage == 1){ // 1 = 100%
		document.getElementById('download-info').classList.remove("active");
	}

	inter+=1;
	
}, 1000);


function unitConversion(n){
	if(Math.floor(n / 2**10) > 0){
		if(Math.floor(n / 2**20) > 0){
			if(Math.floor(n / 2**30) > 0){
				if(Math.floor(n / 2**40) > 0) return `${Math.floor(n*100 / 2**40)/100} TB`;
				else return `${Math.floor(n*100 / 2**30)/100} GB`;
			}else return `${Math.floor(n*100 / 2**20)/100} MB`;
		}else return `${Math.floor(n*100 / 2**10)/100} KB`;
	}else return `${n} B`;
}