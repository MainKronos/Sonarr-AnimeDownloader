import { useState, useEffect } from 'react';
import { Menu } from '@/helper';

import type { ReactNode } from 'react';
import type { API, SerieTableEntry } from '@/utils/API';

import './style.scss';

const MENU_ID = "CTX"

interface TableProps {
    api: API
}

export function Table({ api }: TableProps) {

    const [table, setTable] = useState([] as SerieTableEntry[]);

    // SYNC DATA
    useEffect(() => {
        api.getTable().then(res => setTable(res));
    }, []);

    function test() { console.log('lo') }

    function displayMenu(event: MouseEvent) {
        Menu.show(event, {
            'Copy': test,
            'Edit': test,
            'Delete': test
        })
    }

    return (<>

        {table.map(entry =>
            <details key={entry.title} onContextMenu={displayMenu as any}>
                <summary>
                    <i>movie</i>{entry.title}
                </summary>

                <Tabs 
                    labels={Object.keys(entry.seasons)}
                    contents={Object.values(entry.seasons).map(season => 
                        season.map(link => <a href={link} target="_blank" key={link}>{link}</a>)
                    )}
                />

            </details>
        )}


    </>);
}

interface TabsProps {
    labels: ReactNode[],
    contents: ReactNode[]
}
function Tabs({labels, contents}:TabsProps){

    const [tab, setTab] = useState(0);

    return (<>
        <ul>   
            {labels.map((value, index) => 
                <li 
                    key={value as string} 
                    onClick={() => setTab(index)}
                    className={tab == index ? 'active' : ''}
                >{value}</li>
            )}
            <li><button><i>add</i></button></li>
        </ul>
        <section>
            {contents[tab]}
            <button><i>add</i></button>
        </section>

    </>);
}

