import { API } from "@/utils/API";
import { useEffect, useState } from "react";

import "./index.scss"
import { Icon } from "..";

//https://github.com/MainKronos/Sonarr-AnimeDownloader/blob/1.8.0/documentation/other/react/table.js

interface TableProps {
	api: API
}
export function Table({api}:TableProps) {

	const [entries, setEntries] = useState([] as TableRowProps[]);

	useEffect(() => {
		api.getTable()
		.then(res => setEntries(res))
	}, [api])

	return (
		<div>
			{entries.map(({title, seasons, absolute}, index) => (
				<TableRow
					title={title}
					seasons={seasons}
					absolute={absolute}
					key={index}
				/>	
			))}
		</div>
	);
}

interface TableRowProps {
	title: string,
	seasons: {
		[num:string]: string[]
	},
	absolute: boolean
}
function TableRow({title, seasons, absolute}: TableRowProps){
	return (
		<details>

			<summary>
				<Icon icon="movie"/>
				<span>{title}</span>
				{absolute && ( <span className="badge">absolute</span>)}
			</summary>
			
			<TableRowBody 
				seasons={seasons}
			/>
		</details>
	);
}

interface TableRowBodyProps {
	seasons: {
		[num:string]: string[]
	}
}
function TableRowBody({seasons}: TableRowBodyProps){

	const [active_tab, setActive_tab] = useState(0);

	return (
		<div className="content">
			<div className="tabs">
				{Object.keys(seasons).map((season, index) => 
					<Tab 
						title={season}
						active={index==active_tab} 
						key={index} 
						onClick={()=>setActive_tab(index)}
					/>
				)}
			</div>
			<div className="tabs-content">
				{Object.keys(seasons).map((season, index) => 
					<TabContent 
						links={seasons[season]} 
						active={index==active_tab} 
						key={index} 
					/>
				)}
			</div>
		</div>
	);
}

interface TabProps {
	title: string,
	active: boolean,
	onClick: React.MouseEventHandler<HTMLAnchorElement>
}
function Tab({title, active, onClick}: TabProps) {
	return (
		<a className={active ? "tab active" : "tab"} onClick={onClick}>
			{title.toUpperCase()}
		</a>
	);
}

interface TabContentProps {
	links: string[],
	active: boolean
}
function TabContent({links, active}: TabContentProps){
	return (
		<div className={active ? "tab-content active" : "tab-content"}>
			{links.map(link => 
				<a href={link} target="_blank" key={link}>
					{link}
				</a>
			)}
		</div>
	);
}