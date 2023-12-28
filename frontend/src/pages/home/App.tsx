// import * from "react";
import { useState, useEffect } from 'react';
import { Table, Container, Navigator } from '@/components';

import './style.scss';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';


import { API } from '@/utils/API';
import { ToastContainer } from '@/helper';

export default function App() {

    const [version, setVersion] = useState('');
    const [navActive, setNavActive] = useState(false);

    const api = new API('http://127.0.0.1:5000');

    useEffect(() => {
        api.getVersion().then(res => setVersion(res));
    }, []);

    return (<>
        <Navigator
            activationState={[navActive, setNavActive]}
        >
            <a>Home</a>
            <a href="settings.html">Settings</a>
            <a href="log.html">Log</a>
        </Navigator>
        
        <Container
            title='Tabella Di Conversione'
            version={version}
            navigatorState={[navActive, setNavActive]}
        >
            <Table api={api}/>
        </Container>
        <ToastContainer/>
    </>);

}
