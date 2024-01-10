import { useState, useEffect } from 'react';

import { Container, Navigator, LogViewer } from '@/components';

import { API } from '@/utils/API';
import { ToastContainer } from '@/helper';

import './style.scss';

export default function App() {

    const [version, setVersion] = useState('');
    const [navActive, setNavActive] = useState(false);

    const api = new API(BACKEND);

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
            <LogViewer api={api} />
        </Container>
        <ToastContainer />
    </>);
}