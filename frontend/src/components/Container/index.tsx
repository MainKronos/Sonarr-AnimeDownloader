import { ReactNode } from 'react';

import './style.scss';

interface ContainerProps {
    title: string,
    version: string,
	children?: ReactNode
}

export function Container({title, version, children}:ContainerProps) {
    return (<>
        <header>
            <h1>{title}</h1>
            <a className="btn" id="donate" href="https://github.com/sponsors/MainKronos" target="_blank">
                <i>favorite</i>
            </a>
        </header>

        <main>
            {children}
        </main>
        
        <footer>
            <a href={`https://github.com/MainKronos/Sonarr-AnimeDownloader/releases/tag/${version}`} target="_blank">Ver. {version}</a>
        </footer>

    </>);
}