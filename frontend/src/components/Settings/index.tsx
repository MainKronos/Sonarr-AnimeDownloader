import { useState, useEffect } from 'react';

import { toast } from '@/helper';
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

    useEffect(() => {
        api.getTags().then(res => setTags(res));
    }, []);

    if(tags){
        return (
            <Card>
                <h2>Tags</h2>
                <section id='tags'>
                    {tags.map(tag => <Card key={tag.name} className={tag.active ? 'active' : ''}>
                        <h3 title={tag.id.toString()}>{tag.name}</h3>

                        <button>DELETE</button>
                        <button
                            onClick={() => {
                                setTags([...tags, {...tag, active:!tag.active}]);
                                api.editToggleTag(tag.id)
                                .then(res => toast.success(res.message))
                            }}
                        >{tag.active ? "ON" : "OFF"}</button>

                    </Card>)}
                </section>
            </Card>
        );
    }
}