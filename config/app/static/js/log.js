'use strict';

const converter = new AnsiUp();

class Log extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: false,
      is_loaded: false,
      data: [],
      page: 1
    };
  }

  componentDidMount() {
    this.getLog(this.state.page).then(() => {
      window.scrollTo(0, document.body.scrollHeight);
      window.addEventListener('scroll', () => {
        if (document.documentElement.scrollTop <= 135) {
          if (!this.state.error) {
            let oldHeight = document.body.scrollHeight;
            this.state.page++;
            this.getLog(this.state.page).then(() => {
              let newHeight = document.body.scrollHeight;
              window.scrollTo(0, newHeight - oldHeight);
            });
          }
        }
      });
    });
  }

  getLog(page) {
    return fetch(`/api/log/${page}`).then(res => res.json()).then(res => {
      this.setState({
        error: res.data.length == 0 ? 'Load all data' : res.error,
        is_loaded: true,
        data: [].concat(res.data, this.state.data)
      });
    });
  }

  render() {
    if (!this.state.is_loaded) {
      return /*#__PURE__*/React.createElement("li", null);
    } else {
      return this.state.data.map((row, index, arr) => /*#__PURE__*/React.createElement(Row, {
        key: arr.length - index,
        text: row
      }));
    }
  }

}

function Row(props) {
  return /*#__PURE__*/React.createElement("li", {
    dangerouslySetInnerHTML: {
      __html: converter.ansi_to_html(props.text)
    }
  });
}

const container = document.querySelector('#log');
ReactDOM.render( /*#__PURE__*/React.createElement(React.StrictMode, null, /*#__PURE__*/React.createElement(Log, null)), container);