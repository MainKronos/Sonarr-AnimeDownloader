// import * from "react";
import { useState, useEffect } from 'react';
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'

import { Container, Navigator } from '@/components';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';


import { API } from '@/utils/API';

export default function App() {

    library.add(fas);

	const [version, setVersion] = useState('');

	const api = new API('http://127.0.0.1:5000');

	useEffect(() => {
		api.getVersion().then(res => setVersion(res));
	}, []);

	return (<>
        <Navigator>
            <a>Home</a>
			<a href="settings.html">Settings</a>
			<a href="log.html">Log</a>
        </Navigator>

        <Container
            title='Tabella Di Conversione'
            version={version}
        >

        </Container>
    </>);
		
}
