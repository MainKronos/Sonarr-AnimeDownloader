import { useEffect, useState } from "react";
import { Container, Footer, Header, Navigator, Table } from "@/components";

import '@/styles/base.scss'
import { API } from "@/utils/API";

export default function App() {

	const api = new API(new URL(BACKEND));
	const [version, setVersion] = useState('');

	useEffect(() => {
		api.getVersion()
		.then(res => setVersion(res));
	}, [api]);


	return (<>
		<Header title="Tabella Di Conversione">
			<Navigator>
				<a>Home</a>
				<a href="settings.html">Settings</a>
				<a href="log.html">Log</a>
			</Navigator>
		</Header>
		<Container>
			<Table api={api}/>
		</Container>
		<Footer version={version}/>
	</>)
}	