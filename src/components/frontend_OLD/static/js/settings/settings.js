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
		for(let elem of document.querySelectorAll('input[name=TagsMode]')){
			elem.checked = elem.value == res.data.TagsMode;
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
			ScanDelay: data.hasOwnProperty('ScanDelay') ? data.ScanDelay : null,
			TagsMode: data.hasOwnProperty('TagsMode') ? data.TagsMode : null
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
for(let elem of document.querySelectorAll('input[name=TagsMode]')){
	elem.addEventListener('change', function(event){
		if(this.checked) updateSettings({TagsMode: this.value})
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

class ConnectionsDiv extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			error: false,
			is_loaded: false,
			data: null,
			file: ""
		};
		this.syncData = this.syncData.bind(this);
	}

	componentDidMount() {
		this.syncData();
	}

	syncData() {
		fetch("/api/connections").then(res => res.json()).then(res => {
			this.setState({
				error: res.error,
				is_loaded: true,
				data: res.data
			});
		}, error => {
			this.setState({
				error: error,
				is_loaded: true,
				data: null
			});
		});
	}

	render() {
		const {
			error,
			is_loaded,
			data
		} = this.state;

		if (!is_loaded) {
			return React.createElement(Loading);
		} else {
			return React.createElement(React.Fragment, null, 
				React.createElement("div", {className: "card-title"}, "Connections"), 
				(error) ? React.createElement("div", {className: 'card-content'}, "Error: ", error) : 
				React.createElement(Connections, {
					syncData: this.syncData,
					data: data
				}), 
				React.createElement("section", {className: "bottom"}, 
					React.createElement("a", {
						className: "btn",
						href: "/ie/connections",
						target: "_blank"
					}, "\uF090"), 
					React.createElement("label", {
							htmlFor: "importC",
							className: "btn"
						}, 
						React.createElement("input", {
							id: "importC",
							type: "file",
							accept: ".json",
							value: this.state.file,
							onChange: event => {
								let json = event.target.files[0];

								if (json != null) {
									let formData = new FormData();
									formData.append("file", json, json.name);
									fetch('/ie/connections', {
										method: "POST",
										body: formData
									}).then(response => response.json()).then(res => {
										this.syncData();
										this.setState({
											value: ""
										});
										showToast(res["error"] ? res["error"] : "Connections caricate con successo.");
									});
								}
							}
						}), "\uE2C6"
					)
				)
			);
		}
	}
}

class Connections extends React.Component {
	constructor(props) {
		super(props);
		this.toggle = this.toggle.bind(this);
		this.remove = this.remove.bind(this);
		this.add = this.add.bind(this);
	}

	toggle(connection_name) {
		return fetch('/api/connections/toggle', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				name: connection_name
			})
		}).then(response => response.json()).then(data => {
			showToast(data.data);
			this.props.syncData();
		});
	}

	remove(connection_name) {
		return fetch('/api/connections/remove', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				name: connection_name
			})
		}).then(response => response.json()).then(data => {
			showToast(data.data);
			this.props.syncData();
		});
	}

	add(connection_name, script) {
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
		}).then(response => response.json()).then(data => {
			showToast(data.data);
			this.props.syncData();
		});
	}

	render() {
		return /*#__PURE__*/React.createElement("div", {
			className: "card-content"
		}, this.props.data.map((conn, index) => /*#__PURE__*/React.createElement(Connection, {
			name: conn.name,
			script: conn.script,
			active: conn.active,
			valid: conn.valid,
			key: conn.script + index,
			onToggle: () => this.toggle(conn.name),
			onRemove: () => this.remove(conn.name)
		})), /*#__PURE__*/React.createElement(AddConnections, {
			onAdd: this.add
		}));
	}

}

class AddConnections extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			active: false,
			name: "",
			script: ""
		};
	}

	render() {
		if (this.state.active) {
			return /*#__PURE__*/React.createElement("form", {
				className: "content",
				onSubmit: event => {
					event.preventDefault();
					this.props.onAdd(this.state.name, this.state.script);
					this.setState({
						active: false
					});
				},
				onKeyDown: event => {
					if (event.key == 'Escape') this.setState({
						active: false
					});
				}
			}, /*#__PURE__*/React.createElement("input", {
				autoFocus: true,
				type: "text",
				placeholder: "Name",
				maxLength: "30",
				onChange: event => this.setState({
					name: event.target.value
				}),
				required: true
			}), /*#__PURE__*/React.createElement("input", {
				type: "text",
				placeholder: "script.sh",
				pattern: ".+\\.sh$",
				onChange: event => this.setState({
					script: event.target.value
				}),
				required: true
			}), /*#__PURE__*/React.createElement("button", {
				type: "submit",
				className: "confirm-element btn"
			}, "\ue163"));
		} else {
			return /*#__PURE__*/React.createElement("div", {
				className: "content"
			}, /*#__PURE__*/React.createElement("button", {
				className: "btn add-element",
				onClick: () => this.setState({
					active: true
				})
			}, '\ue145'));
		}
	}

}

function Connection(props) {
	return /*#__PURE__*/React.createElement("div", {
		className: "content",
		onContextMenu: e => {
			menu.show(e, ["Delete"], [props.onRemove]);
		}
	}, /*#__PURE__*/React.createElement("h2", null, props.name), /*#__PURE__*/React.createElement("code", {
		className: props.valid ? '' : 'invalid'
	}, props.script), /*#__PURE__*/React.createElement("span", {
		className: `status ${props.active ? 'active' : ''}`,
		onClick: props.onToggle
	}, props.active ? "ON" : "OFF"));
}

const connections = document.querySelector('#connections');
ReactDOM.render( /*#__PURE__*/React.createElement(React.StrictMode, null, /*#__PURE__*/React.createElement(ConnectionsDiv, null)), connections);

class TagsDiv extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			error: false,
			is_loaded: false,
			data: null,
			file: "",
			enabled: false
		};
		this.syncData = this.syncData.bind(this);
	}

	syncData() {
		fetch("/api/tags").then(res => res.json()).then(res => {
			this.setState({
				error: res.error,
				is_loaded: true,
				data: res.data
			});
		}, error => {
			this.setState({
				error: error,
				is_loaded: true,
				data: null
			});
		});
	}

	componentDidMount() {
		this.syncData()
	}

	render() {
		const {
			error,
			is_loaded,
			data,
			enabled
		} = this.state;

		;

		if (!is_loaded) {
			return /*#__PURE__*/React.createElement(Loading);
		} else {
			return React.createElement(React.Fragment, null, 
				React.createElement("div", { className: 'card-title' }, "Tag Personalizzati"),
				(error) ? React.createElement("div", {className: 'card-content'}, "Error: ", error) : 
				React.createElement(Tags, {
					syncData: this.syncData,
					data: data,
				}), 
				React.createElement("section", { className: "bottom" }, 
					React.createElement("a", {
						className: "btn",
						href: "/ie/tags",
						target: "_blank"
					}, "\uF090"), 
					React.createElement("label", {
							htmlFor: "importT",
							className: "btn"
						}, 
						React.createElement("input", {
							id: "importT",
							type: "file",
							accept: ".json",
							value: this.state.file,
							onChange: event => {
								let json = event.target.files[0];
			
								if (json != null) {
									let formData = new FormData();
									formData.append("file", json, json.name);
									fetch('/ie/tags', {
										method: "POST",
										body: formData
									}).then(response => response.json()).then(res => {
										this.syncData();
										this.setState({
											value: ""
										});
										showToast(res["error"] ? res["error"] : "Tag caricati con successo.");
									});
								}
							}
						}), "\uE2C6"
					)
				)
				
			)
		}
	}

}

class Tags extends React.Component {
	constructor(props) {
		super(props);
		this.toggle = this.toggle.bind(this);
		this.remove = this.remove.bind(this);
		this.add = this.add.bind(this);
	}

	toggle(id, name) {
		return fetch('/api/tags/toggle', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				id: id,
				name: name
			})
		}).then(response => response.json()).then(data => {
			showToast(data.data);
			this.props.syncData();
		});
	}

	remove(id, name) {
		return fetch('/api/tags/remove', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				id: id,
				name: name
			})
		}).then(response => response.json()).then(data => {
			showToast(data.data);
			this.props.syncData();
		});
	}

	add(tag) {
		return fetch('/api/tags/add', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				name: tag,
				active: false,
			})
		}).then(response => response.json()).then(data => {
			showToast(data.data);
			this.props.syncData();
		});
	}

	render() {
		return /*#__PURE__*/React.createElement("div", {
				className: `card-content`
			}
			, this.props.data.map((tag, index) => /*#__PURE__*/React.createElement(Tag, {
				id: tag.id, 
				name: tag.name,
				active: tag.active,
				valid: tag.valid,
				key: tag.name + index,
				onToggle: () => this.toggle(tag.id, tag.name),
				onRemove: () => this.remove(tag.id, tag.name)
			}))
			, /*#__PURE__*/React.createElement(AddTag, {
				onAdd: this.add
			})
		);
	}

}

class AddTag extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			name: "",
			active: false
		};
	}

	render() {

		if (this.state.active) {
			return /*#__PURE__*/React.createElement("form", {
				className: "content",
				onSubmit: event => {
					event.preventDefault();
					this.props.onAdd(this.state.name);
					this.setState({
						active: false
					});
				},
				onKeyDown: event => {
					if (event.key == 'Escape') this.setState({
						active: false
					});
				}
			}, /*#__PURE__*/React.createElement("input", {
				autoFocus: true,
				type: "text",
				placeholder: "Tag",
				maxLength: "30",
				onChange: event => this.setState({
					name: event.target.value
				}),
				required: true
			}),
			/*#__PURE__*/React.createElement("button", {
				type: "submit",
				className: "confirm-element btn"
			}, "\ue163"));
		} else {
			return /*#__PURE__*/React.createElement("div", {
				className: "content"
			}, /*#__PURE__*/React.createElement("button", {
				className: "btn add-element",
				onClick: () => this.setState({
					active: true
				})
			}, '\ue145'));
		}
	}

}

function Tag(props) {
	return React.createElement("div", {
		className: "content",
		onContextMenu: e => {
			menu.show(e, ["Delete"], [props.onRemove]);
		}
	}, 
	React.createElement("h2", null, props.name), 
	React.createElement("code", null, props.valid ? '' : 'Invalido'), 
	React.createElement("span", {
		className: `status ${props.active ? 'active' : ''}`,
		onClick: props.onToggle
	}, props.active ? "ON" : "OFF"));
}


const tags = document.querySelector('#tags');
ReactDOM.render( /*#__PURE__*/React.createElement(React.StrictMode, null, /*#__PURE__*/React.createElement(TagsDiv, null)), tags);