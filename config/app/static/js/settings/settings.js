// range

function syncData() {

	return fetch("/api/settings")
		.then(res => res.json())
		.then((res) => {
			document.getElementById('RenameEp').checked = res.data.RenameEp;
			document.getElementById('MoveEp').checked = res.data.MoveEp;
			document.getElementById('AutoBind').checked = res.data.AutoBind;

			document.getElementById('ScanDelay').value = res.data.ScanDelay;
			document.querySelector("#ScanDelay + label").textContent = res.data.ScanDelay;

			for (let elem of document.querySelectorAll('input[name=LogLevel]')) {
				elem.checked = elem.value == res.data.LogLevel;
			}


		});
}
syncData();

document.getElementById('ScanDelay').addEventListener('input', function (event) {
	document.querySelector("#ScanDelay + label").textContent = this.value;
});

function updateSettings(data) {
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
document.getElementById('ScanDelay').addEventListener('change', function (event) {
	updateSettings({ ScanDelay: parseInt(this.value) });
});
document.getElementById('RenameEp').addEventListener('change', function (event) {
	updateSettings({ RenameEp: this.checked });
});
document.getElementById('MoveEp').addEventListener('change', function (event) {
	updateSettings({ MoveEp: this.checked });
});
document.getElementById('AutoBind').addEventListener('change', function (event) {
	updateSettings({ AutoBind: this.checked });
});
for (let elem of document.querySelectorAll('input[name=LogLevel]')) {
	elem.addEventListener('change', function (event) {
		if (this.checked) updateSettings({ LogLevel: this.value })
	});
}

document.getElementById("importS").addEventListener('change', function () {
	let json = this.files[0];
	if (this.files[0] != null) {
		let formData = new FormData();
		formData.append("file", json, json.name);
		fetch('/ie/settings', { method: "POST", body: formData })
			.then(response => response.json())
			.then((res) => {
				syncData();
				document.getElementById("importS").value = null;
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

		if (error) {
			return /*#__PURE__*/React.createElement("div", null, "Error: ", error);
		} else if (!is_loaded) {
			return /*#__PURE__*/React.createElement("div", null);
		} else {
			return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
				className: "card-title"
			}, "Connections"), /*#__PURE__*/React.createElement(Connections, {
				syncData: this.syncData,
				data: data
			}), /*#__PURE__*/React.createElement("section", {
				className: "bottom"
			}, /*#__PURE__*/React.createElement("a", {
				className: "btn",
				href: "/ie/connections",
				target: "_blank"
			}, "\uF090"), /*#__PURE__*/React.createElement("label", {
				htmlFor: "importC",
				className: "btn"
			}, /*#__PURE__*/React.createElement("input", {
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
			}), "\uE2C6")));
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

		if (error) {
			return /*#__PURE__*/React.createElement("div", null, "Error: ", error);
		} else if (!is_loaded) {
			return /*#__PURE__*/React.createElement(Loading);
		} else {
			return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", { className: 'card-title' }, "Tag Personalizzati"),
					/*#__PURE__*/React.createElement(Tags, {
						syncData: this.syncData,
						data: data,
					})
				// , /*#__PURE__*/React.createElement("section", {
				// className: "bottom"
				// }, /*#__PURE__*/React.createElement("label", {
				// htmlFor: "importC",
				// className: "btn"
				// }, "\uE2C6"))
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

	toggle(tag) {
		return fetch('/api/tags/toggle', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				name: tag
			})
		}).then(response => response.json()).then(data => {
			showToast(data.data);
			this.props.syncData();
		});
	}

	remove(tag) {
		return fetch('/api/tags/remove', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				name: tag
			})
		}).then(response => response.json()).then(data => {
			showToast(data.data);
			this.props.syncData();
		});
	}

	add(tag, inclusive) {
		return fetch('/api/tags/add', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				name: tag,
				inclusive: inclusive,
				active: true,
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
				name: tag.name,
				inclusive: tag.inclusive,
				active: tag.active,
				key: tag.name + index,
				onToggle: () => this.toggle(tag.name),
				onRemove: () => this.remove(tag.name)
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
			inclusive: false,
			active: false
		};
	}

	render() {

		const {
			name,
			inclusive
		} = this.state

		if (this.state.active) {
			return /*#__PURE__*/React.createElement("form", {
				className: "content",
				onSubmit: event => {
					event.preventDefault();
					this.props.onAdd(this.state.name, this.state.inclusive);
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
		/*#__PURE__*/React.createElement("div", { className: "radio-group" },
			/*#__PURE__*/React.createElement("label", { for: this.id, className: "radio" },
				React.createElement('input', {
					type: "radio", id: this.id, name: `inclusive${this.id}`, value: true, checked: inclusive, onClick: () => {
						this.setState({ inclusive: true })
					}
				}),
				"Inclusivo",
				React.createElement("span")
			),
			/*#__PURE__*/React.createElement("label", { for: this.id, className: "radio" },
				React.createElement('input', {
					type: "radio", id: this.id, name: `inclusive${this.id}`, value: false, checked: !inclusive, onClick: () => {
						this.setState({ inclusive: false })
					}
				}),
				"Esclusivo",
				React.createElement("span")
			),
			), /*#__PURE__*/React.createElement("button", {
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
	return /*#__PURE__*/React.createElement("div", {
		className: "content",
		onContextMenu: e => {
			menu.show(e, ["Delete"], [props.onRemove]);
		}
	}, /*#__PURE__*/React.createElement("h2", null, props.name), /*#__PURE__*/React.createElement("code", {}, props.inclusive ? "Inclusivo \u2713" : "Esclusivo \u2A02"), /*#__PURE__*/React.createElement("span", {
		className: `status ${props.active ? 'active' : ''}`,
		onClick: props.onToggle
	}, props.active ? "ON" : "OFF"));
}


const tags = document.querySelector('#tags');
ReactDOM.render( /*#__PURE__*/React.createElement(React.StrictMode, null, /*#__PURE__*/React.createElement(TagsDiv, null)), tags);