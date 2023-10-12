import { ReactElement, ReactNode, useState } from "react";


import "./index.scss"
import { Icon } from "..";

interface NavigatorProps {
	children?: ReactNode
}

export function Navigator(props: NavigatorProps){

	const [active, setActive] = useState(false);

	return (
		<>
			<nav 
			className={active ? 'active':''}
			>
				<div onClick={() => setActive(!active)}></div>
				<div>
					{props.children}
				</div>
			</nav>
			<button onClick={() => setActive(!active)}>
				<Icon icon="menu"/>
			</button>
		</>
	);
}