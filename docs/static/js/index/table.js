'use strict';

var addData;
var syncData;

class Table extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: false,
      is_loaded: false,
      data: null
    };
    this.addData = this.addData.bind(this);
    this.removeData = this.removeData.bind(this);
    this.editData = this.editData.bind(this);
    addData = this.addData;
	syncData = this.syncData.bind(this);;
  }

  componentDidMount() {
    this.syncData();
  }

  syncData() {
    return fetch("static/json/table.json").then(res => res.json()).then(res => {
	  this.setState({is_loaded: false});
      this.setState({
        error: false,
        is_loaded: true,
        data: res
      });
    });
  }

  addData(title, season, links, absolute = false) { 
	return new Promise((res,rej)=>{
		this.syncData();
		showToast("Non disponibile nella versione di test.");
		res();
	});
  }

  removeData(title, season = null, link = null) {
    return new Promise(()=>{
		this.syncData();
		showToast("Non disponibile nella versione di test.");
	});
  }

  editData(title, season = null, link = null) {
    return new Promise(()=>{
		this.syncData();
		showToast("Non disponibile nella versione di test.");
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
      return data.map(anime => /*#__PURE__*/React.createElement(TableRow, {
        title: anime.title,
        seasons: anime.seasons,
        absolute: anime.absolute,
        key: anime.title,
        onAddData: this.addData,
        onEditData: this.editData,
        onRemoveData: this.removeData
      }));
    }
  }

}

function TableRow(props) {
  return /*#__PURE__*/React.createElement("details", null, /*#__PURE__*/React.createElement(TableRowHead, {
    title: props.title,
    absolute: props.absolute,
    onEditData: props.onEditData,
    onRemoveData: props.onRemoveData
  }), /*#__PURE__*/React.createElement(TableRowBody, {
    seasons: props.seasons,
    onAddData: (season, links) => props.onAddData(props.title, season, links, props.absolute),
    onEditData: (season = null, link = null) => props.onEditData(props.title, season, link),
    onRemoveData: (season = null, link = null) => props.onRemoveData(props.title, season, link)
  }));
}

class TableRowHead extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      edit: false,
      value: this.props.title
    };
  }

  render() {
    return /*#__PURE__*/React.createElement("summary", {
      onContextMenu: e => {
        menu.show(e, ["Copy", "Edit", "Delete"], [() => navigator.clipboard.writeText(this.props.title), () => this.setState({
          edit: true
        }), () => this.props.onRemoveData(this.props.title)]);
      }
    }, this.state.edit ? /*#__PURE__*/React.createElement("form", {
      style: {
        display: "inline"
      },
      onSubmit: event => {
        event.preventDefault();
        this.props.onEditData([this.props.title, this.state.value]);
        this.setState({
          edit: false
        });
      },
      onKeyDown: event => {
        if (event.key == 'Escape') this.setState({
          edit: false,
          value: this.props.title
        });
      }
    }, /*#__PURE__*/React.createElement("input", {
      autoFocus: true,
      type: "text",
      placeholder: "this.props.title",
      value: this.state.value,
      onChange: event => this.setState({
        value: event.target.value
      }),
      onBlur: event => {
        if (this.state.value == this.props.title) this.setState({
          edit: false
        });
      }
    })) : this.state.value, this.props.absolute && /*#__PURE__*/React.createElement(Badge, {
      title: "absolute"
    }));
  }

}

class TableRowBody extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tab_active: 0
    };
  }

  render() {
    return /*#__PURE__*/React.createElement("div", {
      className: "content"
    }, /*#__PURE__*/React.createElement("div", {
      className: "tabs"
    }, Object.keys(this.props.seasons).map((season, index) => /*#__PURE__*/React.createElement(Tab, {
      season: season,
      active: index == this.state.tab_active,
      key: index,
      onClick: e => this.setState({
        tab_active: index
      }),
      onEditData: this.props.onEditData,
      onRemoveData: this.props.onRemoveData
    })), /*#__PURE__*/React.createElement(AddSeasonButton, {
      onAddData: this.props.onAddData
    })), /*#__PURE__*/React.createElement("div", {
      className: "tabs-content"
    }, Object.keys(this.props.seasons).map((season, index) => /*#__PURE__*/React.createElement(TabContent, {
      links: this.props.seasons[season],
      active: index == this.state.tab_active,
      key: index,
      onAddData: links => this.props.onAddData(season, links),
      onEditData: (link = null) => this.props.onEditData(season, link),
      onRemoveData: (link = null) => this.props.onRemoveData(season, link)
    }))));
  }

}

class Tab extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      edit: false,
      value: this.props.season
    };
  }

  render() {
    return this.state.edit ? /*#__PURE__*/React.createElement("form", {
      style: {
        display: "inline"
      },
      onSubmit: event => {
        event.preventDefault();
        this.props.onEditData([this.props.season, this.state.value]);
        this.setState({
          edit: false
        });
      },
      onKeyDown: event => {
        if (event.key == 'Escape') this.setState({
          edit: false,
          value: this.props.season
        });
      }
    }, /*#__PURE__*/React.createElement("input", {
      autoFocus: true,
      className: "add-tab",
      type: "number",
      min: "1",
      placeholder: this.props.season,
      value: this.state.value,
      onChange: event => this.setState({
        value: event.target.value
      }),
      onBlur: event => {
        if (this.state.value == this.props.season) this.setState({
          edit: false
        });
      }
    })) : /*#__PURE__*/React.createElement("a", {
      className: this.props.active ? "tab active" : "tab",
      onClick: this.props.onClick,
      onContextMenu: e => {
        menu.show(e, ["Copy", "Edit", "Delete"], [() => navigator.clipboard.writeText(this.state.value.toUpperCase()), () => this.setState({
          edit: true
        }), () => this.props.onRemoveData(this.state.value)]);
      }
    }, this.state.value.toUpperCase());
  }

}

function TabContent(props) {
  return /*#__PURE__*/React.createElement("div", {
    className: props.active ? "tab-content active" : "tab-content"
  }, props.links.map(link => /*#__PURE__*/React.createElement(TabContentLink, {
    link: link,
    onRemoveData: props.onRemoveData,
    onEditData: props.onEditData,
    key: link
  })), /*#__PURE__*/React.createElement(AddLinkButton, {
    onAddData: props.onAddData
  }));
}

class TabContentLink extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      edit: false,
      value: this.props.link
    };
  }

  render() {
    return this.state.edit ? /*#__PURE__*/React.createElement("form", {
      style: {
        display: "inline"
      },
      onSubmit: event => {
        event.preventDefault();
        this.props.onEditData([this.props.link, this.state.value]);
        this.setState({
          edit: false
        });
      },
      onKeyDown: event => {
        if (event.key == 'Escape') this.setState({
          edit: false,
          value: this.props.link
        });
      }
    }, /*#__PURE__*/React.createElement("input", {
      autoFocus: true,
      type: "text",
      placeholder: this.props.link,
      value: this.state.value,
      pattern: "^https:\\/\\/www\\.animeworld\\.tv\\/play\\/.+",
      onChange: event => this.setState({
        value: event.target.value
      }),
      onBlur: event => {
        if (this.state.value == this.props.link) this.setState({
          edit: false
        });
      }
    })) : /*#__PURE__*/React.createElement("a", {
      href: this.state.value,
      target: "_blank",
      onContextMenu: e => {
        menu.show(e, ["Copy", "Edit", "Delete"], [() => navigator.clipboard.writeText(this.state.value), () => this.setState({
          edit: true
        }), () => this.props.onRemoveData(this.state.value)]);
      }
    }, this.state.value);
  }

}

class AddLinkButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      active: false,
      value: ''
    };
  }

  render() {
    return /*#__PURE__*/React.createElement(React.Fragment, null, this.state.active && /*#__PURE__*/React.createElement("form", {
      onSubmit: event => {
        event.preventDefault();
        this.props.onAddData([this.state.value]);
        this.setState({
          active: false,
          value: ''
        });
      },
      onKeyDown: event => {
        if (event.key == 'Escape') this.setState({
          active: false,
          value: ''
        });
      }
    }, /*#__PURE__*/React.createElement("input", {
      autoFocus: true,
      type: "text",
      placeholder: "https://www.animeworld.tv/play/...",
      pattern: "^https:\\/\\/www\\.animeworld\\.tv\\/play\\/.+",
      value: this.state.value,
      onChange: event => this.setState({
        value: event.target.value
      }),
      onBlur: event => {
        if (!this.state.value) this.setState({
          active: false,
          value: ''
        });
      }
    })), /*#__PURE__*/React.createElement("button", {
      className: "btn add-link",
      onClick: () => this.setState({
        active: true
      })
    }, '\ue145'));
  }

}

class AddSeasonButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      active: false,
      value: ''
    };
  }

  render() {
    return /*#__PURE__*/React.createElement(React.Fragment, null, this.state.active && /*#__PURE__*/React.createElement("form", {
      onSubmit: event => {
        event.preventDefault();
        this.props.onAddData(this.state.value, []);
        this.setState({
          active: false,
          value: ''
        });
      },
      onKeyDown: event => {
        if (event.key == 'Escape') this.setState({
          active: false,
          value: ''
        });
      }
    }, /*#__PURE__*/React.createElement("input", {
      autoFocus: true,
      type: "number",
      placeholder: "Season",
      className: "add-tab",
      min: "1",
      value: this.state.value,
      onChange: event => this.setState({
        value: event.target.value
      }),
      onBlur: event => {
        if (!this.state.value) this.setState({
          active: false,
          value: ''
        });
      }
    })), /*#__PURE__*/React.createElement("a", {
      className: "btn add-tab",
      onClick: () => this.setState({
        active: true
      })
    }, '\ue145'));
  }

}

function Badge(props) {
  return /*#__PURE__*/React.createElement("span", {
    className: "badge"
  }, props.title);
}

const container = document.querySelector('#root');
ReactDOM.render( /*#__PURE__*/React.createElement(React.StrictMode, null, /*#__PURE__*/React.createElement(Table, null)), container);