import { useState } from 'react';
import { ReactNode } from 'react';
import './style.scss';

interface NavigatorProps {
	children?: ReactNode
}

export function Navigator({children}:NavigatorProps) {
    const [drawerState, setDrawerState] = useState(false);

	function toggleDrawer() {setDrawerState(!drawerState)}

	return (<>
		<nav className={drawerState ? 'active' : ''} onClick={toggleDrawer}>
            <div></div>
            <div>{children}</div>
        </nav>
        <button onClick={toggleDrawer}>
            <i>menu</i>
        </button>
    </>)
}