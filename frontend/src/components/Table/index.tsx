import { useState, useEffect } from 'react';
import { Menu, toast } from '@/helper';

import type { ReactNode } from 'react';
import type { API, SerieTableEntry } from '@/utils/API';

import './style.scss';

interface TableProps {
    api: API
}

export function Table({ api }: TableProps) {

    const [table, setTable] = useState([] as SerieTableEntry[]);
    const [toSync, setToSync] = useState(true);

    // SYNC DATA
    useEffect(() => {
        if(toSync){
            api.getTable().then(res => setTable(res));
            setToSync(false);
        }
    }, [toSync]);

    return (<>

        {table.map(entry => 
            <TableEntry 
                api={api} 
                entry={entry} 
                onUpdate={() => setToSync(true)}
                key={entry.title}
            />
        )}

    </>);
}

interface TableEntryProps {
    api: API,
    entry: SerieTableEntry
    onUpdate: () => void
}

function TableEntry({api, entry, onUpdate}: TableEntryProps) {
    const [editTitle, setEditTitle] = useState(false);
    const [editSeasons, setEditSasons] = useState(
        Object.fromEntries(
            Object.keys(entry.seasons)
            .map((season) => [season, false])
        )
    );
    const [editLinks, setEditLinks] = useState(
        Object.fromEntries(
            Object.entries(entry.seasons)
            .map(([season, links]) => [
                season,
                Object.fromEntries(
                    links.map((link) => [link, false])
                )
            ])
        )
    );

    return (
        <details>
            <summary
                onContextMenu={e => Menu.show(e as any, {
                    'Copy': () => navigator.clipboard.writeText(entry.title),
                    'Edit': () => setEditTitle(true),
                    'Delete': () => {
                        api.deleteSerie(entry.title)
                        .then(res => {
                            toast.success(res.message);
                            onUpdate();
                        });
                    }
                })}
            >
                <i>movie</i>
                <EditableNode
                    type='text'
                    defaultValue={entry.title}
                    activeState={[editTitle, setEditTitle]}
                    onSubmit={(content) => {
                        api.editSerie(entry.title, content)
                        .then(res => {
                            toast.success(res.message);
                            onUpdate();
                        });
                    }}
                >
                    {entry.title}
                </EditableNode>
            </summary>

            <Tabs
                labels={Object.keys(entry.seasons).map(season =>
                    <EditableNode
                        type='text'
                        defaultValue={season}
                        activeState={[
                            editSeasons[season], 
                            (state:boolean) => setEditSasons({...editSeasons, [season]:state})
                        ]}
                        onSubmit={(content) => {
                            api.editSeason(entry.title, season, content)
                            .then(res => {
                                toast.success(res.message);
                                onUpdate();
                            });
                        }}
                    >
                        <span
                            onContextMenu={e => Menu.show(e as any, {
                                'Copy': () => navigator.clipboard.writeText(season),
                                'Edit': () => setEditSasons({...editSeasons, [season]:true}),
                                'Delete': () => {
                                    api.deleteSeason(entry.title, season)
                                    .then(res => {
                                        toast.success(res.message);
                                        onUpdate();
                                    })
                                }
                            })}
                        >
                            {season}
                        </span>
                    </EditableNode>
                )}
                contents={Object.entries(entry.seasons).map(([season, links]) =>
                    links.map(link =>
                        <EditableNode
                            type='text'
                            defaultValue={link}
                            activeState={[
                                editLinks[season][link], 
                                (state:boolean) => setEditLinks({
                                    ...editLinks, [season]:{
                                        ...editLinks[season], [link]: state
                                    }
                                })
                            ]}
                            onSubmit={(content) => {
                                api.editLink(entry.title, season, link, content)
                                .then(res => {
                                    toast.success(res.message);
                                    onUpdate();
                                });
                            }}
                        >
                            <a 
                                href={link} 
                                target="_blank" 
                                key={link}
                                onContextMenu={e => Menu.show(e as any, {
                                    'Copy': () => navigator.clipboard.writeText(link),
                                    'Edit': () => setEditLinks({
                                        ...editLinks, [season]:{
                                            ...editLinks[season], [link]: true
                                        }
                                    }),
                                    'Delete': () => {
                                        api.deleteLink(entry.title, season, link)
                                        .then(res => {
                                            toast.success(res.message);
                                            onUpdate();
                                        });
                                    }
                                })}
                            >
                                {link}
                            </a>
                        </EditableNode>
                    )
                )}
            />

        </details>
    )
}

interface TabsProps {
    labels: ReactNode[],
    contents: ReactNode[]
}
function Tabs({ labels, contents }: TabsProps) {

    const [tab, setTab] = useState(0);

    return (<>
        <ul>
            {labels.map((value, index) =>
                <li
                    key={index}
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

interface EditableNodeProps<T extends string | number> {
    type: string,
    activeState: [boolean, (active: boolean) => void],
    onSubmit: (content: T) => void,
    defaultValue?: T,
    placeholder?: string,
    pattern?: string,
    children: ReactNode
}
function EditableNode<T extends string | number>({ type, defaultValue, activeState, onSubmit, placeholder, pattern, children }: EditableNodeProps<T>) {
    const [content, setContent] = useState(defaultValue ?? '' as T);
    const [active, setActive] = activeState;

    if (!active) {
        return children;
    } else {
        return (
            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    setActive(false);
                    onSubmit(content);
                }}
            >
                <input
                    autoFocus={true}
                    type={type}
                    value={content}
                    placeholder={placeholder}
                    pattern={pattern}

                    onChange={e => setContent(e.target.value as T)}

                    onBlur={() => setActive(false)}
                    onKeyDown={e => e.key == 'Escape' && setActive(false)}
                />
            </form>
            
        );
    }

}