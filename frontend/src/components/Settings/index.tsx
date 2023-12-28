import { toast } from '@/helper';
import { Card } from '..';

import type { API } from '@/utils/API';

import './style.scss';
import { useState } from 'react';

interface SettingsProps{
    api: API
}

export function Settings({api}:SettingsProps){

    const [settings, setSettings] = useState({
        "AutoBind": true, 
        "LogLevel": "DEBUG", 
        "MoveEp": true, 
        "RenameEp": true, 
        "ScanDelay": 30, 
        "TagsMode": "BLACKLIST"})


    return (
        <Card title='Settings'>
            <section id='settings'>
                <fieldset>
                    <legend>Livello Log</legend>
                    <div>
                        <select>
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
                        <select>
                            <option>BLACKLIST</option>
                            <option>WHITELIST</option>
                        </select>
                    </div>
                    

                </fieldset>

                <fieldset>
                    <legend>Other</legend>
                    <div>
                        <input type="checkbox" name="RenameEp" value="false"/>
                        <label htmlFor="RenameEp">Rinomina Episodi</label>
                    </div>

                    <div>
                        <input type="checkbox" name="MoveEp" value="false"/>
                        <label htmlFor="MoveEp">Sposta Episodi</label>
                    </div>

                    <div>
                        <input type="checkbox" name="AutoBind" value="false"/>
                        <label htmlFor="AutoBind">Auto Ricerca Link</label>
                    </div>

                </fieldset>

                <fieldset>
                    <legend>Intervallo Scan</legend>
                    <div>
                        <input type="number" name="season" id="season" placeholder="1" min="0" step="1"/>
                    </div>

                </fieldset>

                <button>FORCE START</button>
            </section>
        </Card>
    )
}