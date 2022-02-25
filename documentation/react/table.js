'use strict';

var addData;

class Table extends React.Component{
	constructor(props){
		super(props);

		this.state = {
			error: false,
			is_loaded: false,
			data: null
		}
		
		this.addData = this.addData.bind(this);
		this.removeData = this.removeData.bind(this);
		this.editData = this.editData.bind(this);
		addData = this.addData;
	}

	componentDidMount(){
		this.syncData();
	}

	syncData(){
		fetch("/api/table")
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

	addData(title, season, links, absolute=false){
		return fetch('/api/table/add', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				title: title,
				season: season,
				links: links,
				absolute: absolute
			})
		})
		.then(response => response.json())
		.then(data => {
			showToast(data.data)
			this.syncData();

		});
	}

	removeData(title, season=null, link=null){
		return fetch('/api/table/remove', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				title: title,
				season: season,
				link: link
			})
		})
		.then(response => response.json())
		.then(data => {
			showToast(data.data)
			this.syncData();

		});
	}

	editData(title, season=null, link=null){
		return fetch('/api/table/edit', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				title: title,
				season: season,
				link: link
			})
		})
		.then(response => response.json())
		.then(data => {
			showToast(data.data)
			this.syncData();

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
				data.map(anime => 
					<TableRow 
						title={anime.title} 
						seasons={anime.seasons} 
						absolute={anime.absolute} 
						key={anime.title} 
						onAddData={this.addData}
						onEditData={this.editData}
						onRemoveData={this.removeData}
					/>
				)
			);
		}
	}
}

function TableRow(props){
	return (
		<details>
			<TableRowHead 
				title={props.title} 
				absolute={props.absolute}
				onEditData={props.onEditData}
				onRemoveData={props.onRemoveData}
			/>
			<TableRowBody 
				seasons={props.seasons} 
				onAddData={(season, links) => props.onAddData(props.title, season, links, props.absolute)}
				onEditData={(season=null, link=null)=>props.onEditData(props.title, season, link)}
				onRemoveData={(season=null, link=null)=>props.onRemoveData(props.title, season, link)}
			/>
		</details>
	);
}



class TableRowHead extends React.Component{
	constructor(props){
		super(props);

		this.state = {
			edit: false,
			value: this.props.title
		}
	}

	render(){
		return (
			<summary onContextMenu={(e)=>{
				menu.show(e, ["Copy","Edit","Delete"], [
					()=>navigator.clipboard.writeText(this.props.title),
					()=>this.setState({edit: true}),
					()=>this.props.onRemoveData(this.props.title)
				]);
			}}>
				{this.state.edit ? (
					<form
						style={{display: "inline"}} 
						onSubmit={(event)=>{
							event.preventDefault();
							this.props.onEditData([this.props.title, this.state.value]);
							this.setState({edit: false});	
						}}
						onKeyDown={(event)=>{
							if(event.key == 'Escape') this.setState({edit: false, value: this.props.title});
						}}>
						<input autoFocus 
							type="text" 
							placeholder="this.props.title" 
							value={this.state.value} 
							onChange={(event)=>this.setState({value: event.target.value})} 
							onBlur={(event)=>{
								if(this.state.value == this.props.title) this.setState({edit: false});
							}}
						/>
					</form>
				) : this.state.value}

				{this.props.absolute && (
					<Badge title="absolute"/>
				)}
			</summary>
		);
	}
}

class TableRowBody extends React.Component{
	constructor(props){
		super(props);

		this.state = {
			tab_active: 0
		}
	}

	render(){
		return (
			<div className="content">
				<div className="tabs">
					{Object.keys(this.props.seasons).map((season, index) => 
						<Tab 
							season={season}
							active={index==this.state.tab_active} 
							key={index} 
							onClick={(e)=>this.setState({tab_active: index})}
							onEditData={this.props.onEditData}
							onRemoveData={this.props.onRemoveData}
						/>
					)}
					<AddSeasonButton onAddData={this.props.onAddData}/>
				</div>
				<div className="tabs-content">
					{Object.keys(this.props.seasons).map((season, index) => 
						<TabContent 
							links={this.props.seasons[season]} 
							active={index==this.state.tab_active} 
							key={index} 
							onAddData={(links) => this.props.onAddData(season, links)}
							onEditData={(link=null)=>this.props.onEditData(season, link)}
							onRemoveData={(link=null)=>this.props.onRemoveData(season, link)}
						/>
					)}
				</div>
			</div>
		);
	}
}

class Tab extends React.Component{
	constructor(props){
		super(props);

		this.state = {
			edit: false,
			value: this.props.season
		}
	}

	render(){
		return (
			this.state.edit ? (
				<form
					style={{display: "inline"}} 
					onSubmit={(event)=>{
						event.preventDefault();
						this.props.onEditData([this.props.season, this.state.value]);
						this.setState({edit: false});
					}}
					onKeyDown={(event)=>{
						if(event.key == 'Escape') this.setState({edit: false, value: this.props.season});
					}}>
					<input autoFocus 
						className="add-tab"
						type="number"
						min="1"
						placeholder={this.props.season} 
						value={this.state.value} 
						onChange={(event)=>this.setState({value: event.target.value})} 
						onBlur={(event)=>{
							if(this.state.value == this.props.season) this.setState({edit: false});
						}}
					/>
				</form>
			) : (
				<a 
				className={this.props.active ? "tab active" : "tab"} 
				onClick={this.props.onClick}
				onContextMenu={(e)=>{
					menu.show(e, ["Copy", "Edit", "Delete"], [
						()=>navigator.clipboard.writeText(this.state.value.toUpperCase()),
						()=>this.setState({edit: true}),
						()=>this.props.onRemoveData(this.state.value)
					]);
				}}>
					{this.state.value.toUpperCase()}
				</a>
			)
		);
	}
}

function TabContent(props){
	return (
		<div className={props.active ? "tab-content active" : "tab-content"}>
			{props.links.map(link => 
				<TabContentLink 
					link={link}
					onRemoveData={props.onRemoveData}
					onEditData={props.onEditData}
					key={link}
				/>
			)}
			<AddLinkButton onAddData={props.onAddData}/>
		</div>
	);
}

class TabContentLink extends React.Component{
	constructor(props){
		super(props);

		this.state = {
			edit: false,
			value: this.props.link
		}
	}

	render(){
		return (
			this.state.edit ? (
				<form
					style={{display: "inline"}} 
					onSubmit={(event)=>{
						event.preventDefault();
						this.props.onEditData([this.props.link, this.state.value]);
						this.setState({edit: false});
					}}
					onKeyDown={(event)=>{
						if(event.key == 'Escape') this.setState({edit: false, value: this.props.link});
					}}>
					<input autoFocus 
						type="text"
						placeholder={this.props.link} 
						value={this.state.value} 
						pattern="^https:\/\/www\.animeworld\.tv\/play\/.+"
						onChange={(event)=>this.setState({value: event.target.value})} 
						onBlur={(event)=>{
							if(this.state.value == this.props.link) this.setState({edit: false});
						}}
					/>
				</form>
			) : (
				<a 	href={this.state.value} 
					target="_blank" 
					onContextMenu={(e)=>{menu.show(e, ["Copy","Edit","Delete"], [
						()=>navigator.clipboard.writeText(this.state.value),
						()=>this.setState({edit: true}),
						()=>this.props.onRemoveData(this.state.value)
					]);
				}}>
					{this.state.value}
				</a>
			)
		);
	}

}




class AddLinkButton extends React.Component{
	constructor(props){
		super(props);

		this.state = {
			active: false,
			value: ''
		}
	}
	render(){
		return (
			<React.Fragment>
				{this.state.active && (
					<form 
						onSubmit={(event)=>{
							event.preventDefault();
							this.props.onAddData([this.state.value]);
							this.setState({active: false, value: ''});
							
						}}
						onKeyDown={(event)=>{
							if(event.key == 'Escape') this.setState({active: false, value: ''});
						}}>
						<input autoFocus 
							type="text" 
							placeholder="https://www.animeworld.tv/play/..." 
							pattern="^https:\/\/www\.animeworld\.tv\/play\/.+"
							value={this.state.value} 
							onChange={(event)=>this.setState({value: event.target.value})} 
							onBlur={(event)=>{
								if(!this.state.value) this.setState({active: false, value: ''});
							}}
						/>
					</form>
				)}
				<button className="btn add-link" onClick={()=>this.setState({active: true})}>
					{'\ue145'}
				</button>
			</React.Fragment>
		);
	}
}

class AddSeasonButton extends React.Component{
	constructor(props){
		super(props);

		this.state = {
			active: false,
			value: ''
		}

	}
	render(){
		return (
			<React.Fragment>
				{this.state.active && (
					<form 
						onSubmit={(event)=>{
							event.preventDefault();
							this.props.onAddData(this.state.value, []);
							this.setState({active: false, value: ''});
							
						}}
						onKeyDown={(event)=>{
							if(event.key == 'Escape') this.setState({active: false, value: ''});
						}}>
						<input autoFocus 
							type="number" 
							placeholder="Season" 
							className="add-tab"
							min="1"
							value={this.state.value} 
							onChange={(event)=>this.setState({value: event.target.value})} 
							onBlur={(event)=>{
								if(!this.state.value) this.setState({active: false, value: ''});
							}}
						/>
					</form>
				)}
				<a className="btn add-tab" onClick={()=>this.setState({active: true})}>{'\ue145'}</a>
			</React.Fragment>
		);
	}
}

function Badge(props){
	return <span className="badge">{props.title}</span>
}

const container = document.querySelector('#root');
ReactDOM.render(
	(
		<React.StrictMode>
			<Table/>
		</React.StrictMode>
	), container
);