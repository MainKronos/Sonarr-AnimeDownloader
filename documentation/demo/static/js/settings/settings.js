// range

function syncData(){

	return fetch("/static/json/settings.json")
	.then(res => res.json())
	.then((res) => {
		document.getElementById('RenameEp').checked = res.RenameEp;
		document.getElementById('MoveEp').checked = res.MoveEp;
		document.getElementById('AutoBind').checked = res.AutoBind;

		document.getElementById('ScanDelay').value = res.ScanDelay;
		document.querySelector("#ScanDelay + label").textContent = res.ScanDelay;

		for(let elem of document.querySelectorAll('input[name=LogLevel]')){
			elem.checked = elem.value == res.LogLevel;
		}


	});
}
syncData();

document.getElementById('ScanDelay').addEventListener('input', function(event){
	document.querySelector("#ScanDelay + label").textContent = this.value;
});

function updateSettings(data){
	return new Promise((res,rej)=>{
		showToast("Non disponibile nella versione di test.");
		syncData();
		res();
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

		syncData();
		document.getElementById("importS").value  = null;
		showToast("Non disponibile nella versione di test.");
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
	  fetch("/static/json/connections.json").then(res => res.json()).then(res => {
		this.setState({
		  error: "",
		  is_loaded: true,
		  data: res
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
		  href: "/static/json/connections.json",
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
			  showToast("Non disponibile nella versione di test.");
			  this.setState({
				value: ""
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
		return new Promise((res,rej)=>{
			showToast("Non disponibile nella versione di test.");
			this.props.syncData();
			res();
		});
	}
  
	remove(connection_name) {
		return new Promise((res,rej)=>{
			showToast("Non disponibile nella versione di test.");
			this.props.syncData();
			res();
		});
	}
  
	add(connection_name, script) {
		return new Promise((res,rej)=>{
			showToast("Non disponibile nella versione di test.");
			this.props.syncData();
			res();
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
		  className: "confirm-connection btn"
		}, "\ue163"));
	  } else {
		return /*#__PURE__*/React.createElement("div", {
		  className: "content"
		}, /*#__PURE__*/React.createElement("button", {
		  className: "btn add-connection",
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