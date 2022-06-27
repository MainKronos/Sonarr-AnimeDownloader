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

document.getElementById("importS").addEventListener('change', function(){
	let json = this.files[0];
	if(this.files[0] != null){
		let formData = new FormData();
		formData.append("file", json, json.name);
		fetch('/ie/settings', {method: "POST", body: formData})
		.then(response => response.json())
		.then((res)=>{
			syncData();
			document.getElementById("importS").value  = null;
			showToast(res["error"] ? res["error"] : "Impostazioni caricate con successo.")
		})
	}
});


// REACT /////////////////////////////

class ConnectionsDiv extends React.Component{
	constructor(props){
		super(props);

		this.state = {
			error: false,
			is_loaded: false,
			data: null,
			file: ""
		}

		this.syncData = this.syncData.bind(this);
	}


	componentDidMount(){
		this.syncData();
	}

	syncData(){
		fetch("/api/connections")
		.then(res => res.json())
		.then((res) => {
			this.setState({
				error: res.error,
				is_loaded: true,
				data: res.data
			});
		}, (error) => {
			this.setState({
				error: error,
				is_loaded: true,
				data: null
			});
		});
	}

	render(){
		const { error, is_loaded, data } = this.state;
		if (error) {
			return <div>Error: {error}</div>;
		} else if (!is_loaded) {
			return <div></div>;
		} else {
			return (
				<React.Fragment>
					<div className="card-title">Connections</div>
					<Connections
						syncData={this.syncData}
						data = {data}
					/>
					<section className="bottom">
						<a className="btn" href="/ie/connections" target="_blank">&#xf090;</a>
						<label htmlFor="importC" className="btn">
							<input 
								id="importC" 
								type="file" 
								accept=".json"
								value={this.state.file} 
								onChange={(event)=>{
									let json = event.target.files[0];
									if(json != null){
										let formData = new FormData();
										formData.append("file", json, json.name);
										fetch('/ie/connections', {method: "POST", body: formData})
										.then(response => response.json())
										.then((res)=>{
											this.syncData();
											this.setState({value: ""});
											showToast(res["error"] ? res["error"] : "Connections caricate con successo.")
										})
									}
								}}
							/>&#xe2c6;
						</label>
					</section>
				</React.Fragment>
			);
		}
	}
}

class Connections extends React.Component{
	constructor(props){
		super(props);

		this.toggle = this.toggle.bind(this);
		this.remove = this.remove.bind(this);
		this.add = this.add.bind(this);
	}

	toggle(connection_name){
		return fetch('/api/connections/toggle', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				name: connection_name
			})
		})
		.then(response => response.json())
		.then(data => {
			showToast(data.data);
			this.props.syncData();
		});
	}

	remove(connection_name){
		return fetch('/api/connections/remove', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				name: connection_name
			})
		})
		.then(response => response.json())
		.then(data => {
			showToast(data.data);
			this.props.syncData();
		});
	}

	add(connection_name, script){
		return fetch('/api/connections/add', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				name: connection_name,
				script: script,
				active: false
			})
		})
		.then(response => response.json())
		.then(data => {
			showToast(data.data);
			this.props.syncData();
		});
	}

	render(){
		return (
			<div className="card-content">
				{this.props.data.map((conn, index) => 
					<Connection 
						name={conn.name}
						script={conn.script}
						active={conn.active}
						valid={conn.valid}
						key={conn.script + index}
						onToggle={() => this.toggle(conn.name)}
						onRemove={() => this.remove(conn.name)}
					/>
				)}
				<AddConnections
					onAdd={this.add}
				/>
			</div>
		);
	}
}

class AddConnections extends React.Component{
	constructor(props){
		super(props);

		this.state = {
			active: false,
			name: "",
			script: ""
		}
	}

	render(){

		if(this.state.active){
			return (
				<form 
					className="content"
					onSubmit={(event)=>{
						event.preventDefault();
						this.props.onAdd(this.state.name, this.state.script);
						this.setState({active: false});
						
					}}
					onKeyDown={(event)=>{
						if(event.key == 'Escape') this.setState({active: false});
					}}>
					<input autoFocus 
						type="text" 
						placeholder="Name" 
						maxLength="30"
						onChange={(event)=>this.setState({name: event.target.value})}
						required
					/>
					<input 
						type="text" 
						placeholder="script.sh" 
						pattern=".+\.sh$"
						onChange={(event)=>this.setState({script: event.target.value})}
						required
					/>
					<button type="submit" className="confirm-connection btn">
						{"\ue163"}
					</button>
				</form>
			);
		}else{
			return (
				<div className="content">
					<button className="btn add-connection" onClick={()=>this.setState({active: true})}>
						{'\ue145'}
					</button>
				</div>
			);
		}
	}
}


function Connection(props){
	return(
		<div 
			className="content"
			onContextMenu={(e)=>{
				menu.show(e, ["Delete"], [
					props.onRemove
				]);
			}}
		>
			<h2>{props.name}</h2>
			<code className={props.valid?'':'invalid'}>{props.script}</code>
			<span 
				className={`status ${props.active?'active':''}`}
				onClick={props.onToggle}
			>
				{props.active?"ON":"OFF"}
			</span>
		</div>

	)
}

const connections = document.querySelector('#connections');
ReactDOM.render(
	(
		<React.StrictMode>	
			<ConnectionsDiv/>
		</React.StrictMode>
	), connections
);