import { useState, useEffect } from 'react';

import { Menu, toast } from '@/helper';
import { Card } from '..';

import type { API, SettingsOptions, TagValue } from '@/utils/API';

import './style.scss';

interface SettingsProps {
    api: API
}

export function Settings({ api }: SettingsProps) {

    return (<>
        <SettingCard api={api} />

        <TagsCard api={api} />
    </>)
}


function SettingCard({ api }: SettingsProps) {
    const [settings, setSettings] = useState<SettingsOptions>();

    useEffect(() => {
        api.getSettings().then(res => setSettings(res));
    }, []);

    if (settings)
        return (
            <Card>
                <h2>Settings</h2>
                <section id='settings'>
                    <fieldset>
                        <legend>Livello Log</legend>
                        <div>
                            <select
                                value={settings.LogLevel}
                                onChange={(e) => {
                                    setSettings({ ...settings, LogLevel: e.target.value as any });
                                    api.editSettings("LogLevel", e.target.value)
                                        .then(res => toast.success(res.message));
                                }}
                            >
                                <option>DEBUG</option>
                                <option>INFO</option>
                                <option>WARNING</option>
                                <option>ERROR</option>
                                <option>CRITICAL</option>
                            </select>
                        </div>
                    </fieldset>

                    <fieldset>
                        <legend>Modalità Tag</legend>
                        <div>
                            <select
                                value={settings.TagsMode}
                                onChange={(e) => {
                                    setSettings({ ...settings, TagsMode: e.target.value as any });
                                    api.editSettings("TagsMode", e.target.value)
                                        .then(res => toast.success(res.message));
                                }}
                            >
                                <option>BLACKLIST</option>
                                <option>WHITELIST</option>
                            </select>
                        </div>


                    </fieldset>

                    <fieldset>
                        <legend>Other</legend>
                        <div>
                            <input type="checkbox" name="RenameEp" id="RenameEp" checked={settings.RenameEp} onChange={e => {
                                setSettings({ ...settings, RenameEp: e.target.checked });
                                api.editSettings("RenameEp", e.target.checked)
                                    .then(res => toast.success(res.message));
                            }} />
                            <label htmlFor="RenameEp">Rinomina Episodi</label>
                        </div>

                        <div>
                            <input type="checkbox" name="MoveEp" id="MoveEp" checked={settings.MoveEp} onChange={e => {
                                setSettings({ ...settings, MoveEp: e.target.checked });
                                api.editSettings("MoveEp", e.target.checked)
                                    .then(res => toast.success(res.message));
                            }} />
                            <label htmlFor="MoveEp">Sposta Episodi</label>
                        </div>

                        <div>
                            <input type="checkbox" name="AutoBind" id="AutoBind" checked={settings.AutoBind} onChange={e => {
                                setSettings({ ...settings, AutoBind: e.target.checked });
                                api.editSettings("AutoBind", e.target.checked)
                                    .then(res => toast.success(res.message));
                            }} />
                            <label htmlFor="AutoBind">Auto Ricerca Link</label>
                        </div>

                    </fieldset>

                    <fieldset>
                        <legend>Intervallo Scan</legend>
                        <div>
                            <input type="number" name="ScanDelay" id="ScanDelay" placeholder="1" min="30" step="5" value={settings.ScanDelay} onChange={e => {
                                if (e.target.checkValidity()) {
                                    setSettings({ ...settings, ScanDelay: e.target.valueAsNumber });
                                    api.editSettings("ScanDelay", e.target.valueAsNumber)
                                        .then(res => toast.success(res.message));
                                }
                            }} />
                        </div>

                    </fieldset>

                    <button onClick={() => {
                        api.putWekeup()
                            .then(res => toast(res.message));
                    }}>FORCE START</button>
                </section>
            </Card>
        );
}



function TagsCard({ api }: SettingsProps) {
    const [tags, setTags] = useState<TagValue[]>();
    const [toSync, setToSync] = useState(true);

    useEffect(() => {
        if(toSync) {
            api.getTags().then(res => setTags(res));
            setToSync(false);
        }
    }, [toSync]);

    async function toggleTag(tag:TagValue) {
        let res = await api.editToggleTag(tag.id);
        toast.success(res.message);
        setToSync(true);
    }

    async function deleteTag(tag:TagValue) {
        let res = await api.deleteTag(tag.id);
        toast.success(res.message);
        setToSync(true);
    }

    async function addTag(name:string) {
        let res = await api.addTag(name, false);
        toast.info(res.message);
        setToSync(true);
    }

    if(tags){
        return (
            <Card>
                <h2>Tags</h2>
                <section id='tags'>
                    {tags.map(tag => 
                        <Card key={tag.name} className={tag.active ? 'active' : ''}>
                            <h3 
                                title={tag.id.toString()}
                                onContextMenu={e => Menu.show(e as any, {
                                    'Copy': () => navigator.clipboard.writeText(tag.name),
                                    'Delete': () => deleteTag(tag)
                                })}
                            >{tag.name}</h3>

                            <button
                                onClick={() => toggleTag(tag)}
                            >{tag.active ? "ON" : "OFF"}</button>

                        </Card>
                    )}

                    <AddCard onSubmit={addTag}/>
                </section>
            </Card>
        );
    }
}

interface AddCardProps {
    onSubmit: (content:string) => void
}
function AddCard({onSubmit}:AddCardProps) {
    const [active, setActive] = useState(false);
    const [content, setContent] = useState('');

    function reset() {
        setContent('');
        setActive(false);
    }

    if(!active){
        return (
            <Card>
                <button type="button" onClick={() => setActive(true)}><i>add</i></button>
            </Card>
        )
    }else {
        return (
            <form onSubmit={(e) => {
                e.preventDefault();
                if(content) onSubmit(content);
                reset();
            }} 
                className='card'
                onKeyDown={e => e.key == 'Escape' && reset()}
            >
                <textarea autoFocus={true} onChange={e => setContent(e.target.value)}></textarea>
                <button type='submit'>SUBMIT</button>
            </form>

        )
    }
}