import { useState, useEffect } from 'react';
import { Menu, toast } from '@/helper';
import { Modal, Badge } from '..';

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
        if (toSync) {
            api.getTable().then(res => setTable(res));
            setToSync(false);
        }
    }, [toSync]);

    return (<>
        
        <SerieAddModal
            api={api}
            onUpdate={() => setToSync(true)}
        />

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

interface SerieAddModalProps{
    api: API,
    onUpdate: () => void
}

function SerieAddModal({api, onUpdate}:SerieAddModalProps){
    const [modalActive, setModalActive] = useState(false);

    const [info, setInfo] = useState({
        title: '',
        season: NaN,
        absolute: false,
        link: ''
    })

    async function submit(e:any){
        e.preventDefault();
        let msg = (await api.addSerie(info.title, info.absolute)).message;
        toast.success(msg);
        msg = (await api.addSeason(info.title, info.season.toString())).message;
        toast.success(msg);
        msg = (await api.addLinks(info.title, info.season.toString(), [info.link])).message;
        toast.success(msg);

        setModalActive(false);
        onUpdate();
    }

    return (<>
        <Modal
            activationState={[modalActive, setModalActive]}
        >
            <form onSubmit={submit}>
                <div>
                    <input type="text" name="title" id="title" placeholder="Sword Art Online" required onChange={(e) => setInfo({...info, title: e.target.value})}/>
                    <label htmlFor="title">Nome Anime</label>
                </div>
                <div>
                    <input type="number" name="season" id="season" placeholder="1" min="0" step="1" required disabled={info.absolute} onChange={(e) => setInfo({...info, season: e.target.valueAsNumber})}/>
                    <label htmlFor="season">Stagione</label>
                    
                </div>
                <div>
                    <input type="checkbox" id="absolute" name="absolute" onChange={(e) => setInfo({...info,absolute: e.target.checked})}/>
                    <label htmlFor="absolute">Absolute</label>
                </div>
                <div>
                    <input type="text" name="link" id="link" placeholder="https://www.animeworld.so/play/sword-art-online.N0onT" pattern="^https:\/\/www\.animeworld\.(tv|so)\/play\/.+" required onChange={(e) => setInfo({...info, link: e.target.value})}/>
                    <label htmlFor="link">Link</label>
                </div>
                <div>
                    <button type="reset" id="clear" onClick={() => setModalActive(false)}>CLEAR</button>
                    <button type="submit" id="submit">SUBMIT</button>
                </div>
		    </form>

        </Modal>

        <button 
            id="add-anime" 
            type='button' 
            onClick={()=>setModalActive(true)}
        >
            <i>add</i>
        </button>
    </>);
}

interface TableEntryProps {
    api: API,
    entry: SerieTableEntry
    onUpdate: () => void
}

function TableEntry({ api, entry, onUpdate }: TableEntryProps) {
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
                    activationState={[editTitle, setEditTitle]}
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

                {entry.absolute && <Badge title='ABSOLUTE'/>}
            </summary>

            <Tabs
                labels={Object.keys(entry.seasons).map(season =>
                    <EditableNode
                        type='text'
                        defaultValue={season}
                        activationState={[
                            editSeasons[season],
                            (state: boolean) => setEditSasons({ ...editSeasons, [season]: state })
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
                                'Edit': () => setEditSasons({ ...editSeasons, [season]: true }),
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
                onAddLabel={(content) => {
                    api.addSeason(entry.title, content)
                    .then(res => {
                        toast.success(res.message);
                        onUpdate();
                    })
                }}
                contents={Object.entries(entry.seasons).map(([season, links]) =>
                    links.map(link =>
                        <EditableNode
                            key={link}
                            type='text'
                            defaultValue={link}
                            activationState={[
                                editLinks[season][link],
                                (state: boolean) => setEditLinks({
                                    ...editLinks, [season]: {
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
                                onContextMenu={e => Menu.show(e as any, {
                                    'Copy': () => navigator.clipboard.writeText(link),
                                    'Edit': () => setEditLinks({
                                        ...editLinks, [season]: {
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
                onAddContent={(index, content) => {
                    api.addLinks(entry.title, Object.keys(entry.seasons)[index], [content])
                    .then(res => {
                        toast.success(res.message);
                        onUpdate();
                    })
                }}
            />

        </details>
    )
}

interface TabsProps {
    labels: ReactNode[],
    contents: ReactNode[]
    onAddLabel?: (content:string) => void,
    onAddContent?: (index:number, content:string) => void,
}
function Tabs({ labels, contents, onAddLabel, onAddContent }: TabsProps) {

    const [tab, setTab] = useState(0);
    const [addLabel, setAddLabel] = useState(false);
    const [addContent, setAddContent] = useState(false);

    return (<>
        <ul>
            {labels.map((value, index) =>
                <li
                    key={index}
                    onClick={() => setTab(index)}
                    className={tab == index ? 'active' : ''}
                >{value}</li>
            )}
            {onAddLabel && (
                <li>
                    <EditableNode
                        type='text'
                        defaultValue=''
                        activationState={[addLabel, setAddLabel]}
                        onSubmit={onAddLabel}
                    >
                        <button type='button' onClick={() => setAddLabel(true)}><i>add</i></button>
                    </EditableNode>
                </li>
            )}
            
        </ul>
        <section>
            {contents[tab]}
            {onAddContent && (
                <EditableNode
                    type='text'
                    defaultValue=''
                    activationState={[addContent, setAddContent]}
                    onSubmit={(content) => onAddContent(tab, content)}
                >
                    <button type='button' onClick={() => setAddContent(true)}><i>add</i></button>
                </EditableNode>
            )}
            
        </section>

    </>);
}

interface EditableNodeProps<T extends string | number> {
    type: string,
    activationState: [boolean, (active: boolean) => void],
    onSubmit: (content: T) => void,
    defaultValue?: T,
    placeholder?: string,
    pattern?: string,
    children: ReactNode
}

function EditableNode<T extends string | number>({ type, defaultValue, activationState, onSubmit, placeholder, pattern, children }: EditableNodeProps<T>) {
    const [content, setContent] = useState(defaultValue ?? '' as T);
    const [active, setActive] = activationState;

    function reset() {
        setActive(false);
        setContent(defaultValue ?? '' as T);
    }

    if (!active) {
        return children;
    } else {
        return (
            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    onSubmit(content);
                    reset();
                }}
            >
                <input
                    autoFocus={true}
                    type={type}
                    value={content}
                    placeholder={placeholder}
                    pattern={pattern}

                    onChange={e => setContent(e.target.value as T)}

                    onBlur={reset}
                    onKeyDown={e => e.key == 'Escape' && reset()}
                />
            </form>

        );
    }

}