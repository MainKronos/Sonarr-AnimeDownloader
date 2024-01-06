import { useState, useEffect } from 'react';

import { Container, Navigator } from '@/components';

import { API } from '@/utils/API';
import { ToastContainer } from '@/helper';

import './style.scss';

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
            <a href="index.html">Home</a>
            <a href="settings.html">Settings</a>
            <a>Log</a>
        </Navigator>
        
        <Container
            title='Settings'
            version={version}
            navigatorState={[navActive, setNavActive]}
        >
           
        </Container>
        <ToastContainer/>
    </>);
}