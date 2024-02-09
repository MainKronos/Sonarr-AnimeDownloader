import type { ReactNode } from 'react';
import './style.scss';

interface NavigatorProps {
    activationState: [boolean, (state:boolean)=> void]
	children?: ReactNode
}

export function Navigator({activationState, children}:NavigatorProps) {
    const [drawerState, setDrawerState] = activationState;

	function toggleDrawer() {setDrawerState(!drawerState)}

	return (<>
		<nav className={drawerState ? 'active' : ''} onClick={toggleDrawer}>
            <div></div>
            <div>{children}</div>
        </nav>
    </>)
}