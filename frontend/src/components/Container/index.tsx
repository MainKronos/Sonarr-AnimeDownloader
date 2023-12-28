import { ReactNode } from 'react';

import './style.scss';

interface ContainerProps {
    title: string,
    version: string,
    navigatorState?: [boolean, (state:boolean)=> void]
	children?: ReactNode,
}

export function Container({title, version, navigatorState, children}:ContainerProps) {

    return (<>
        <header>
            <h1>{title}</h1>
            <a className="btn" id="donate" href="https://github.com/sponsors/MainKronos" target="_blank">
                <i>favorite</i>
            </a>
            {navigatorState &&
                <button onClick={() => navigatorState[1](!navigatorState[0])}>
                    <i>menu</i>
                </button>
            }
        </header>

        <main>
            {children}
        </main>
        
        <footer>
            <a href={`https://github.com/MainKronos/Sonarr-AnimeDownloader/releases/tag/${version}`} target="_blank">Ver. {version}</a>
        </footer>

    </>);
}