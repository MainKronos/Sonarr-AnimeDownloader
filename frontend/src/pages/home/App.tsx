// import * from "react";
import { useState, useEffect } from 'react';

import { Header, Footer } from '@/components';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import IconButton from '@mui/material/IconButton';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import Container from '@mui/material/Container';
import ListItemIcon from '@mui/material/ListItemIcon';
import Skeleton from '@mui/material/Skeleton';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Divider from '@mui/material/Divider';

import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';

import MenuIcon from '@mui/icons-material/Menu';
import SettingsIcon from '@mui/icons-material/Settings';
import InboxIcon from '@mui/icons-material/Inbox';
import ArticleIcon from '@mui/icons-material/Article';

import { API } from '@/utils/API';

import type {SerieTableEntry, SeasonsTableEntry} from '@/utils/types';

export default function App() {

	const darkTheme = createTheme({ palette: { mode: 'dark' } });

	const [drawerOpen, setDrawerOpen] = useState(false);
	const [version, setVersion] = useState('');

	const api = new API('http://127.0.0.1:5000');

	useEffect(() => {
		api.getVersion().then(res => setVersion(res));
	}, []);

	return (
		<ThemeProvider theme={darkTheme}>
			<CssBaseline />

			<Header title='Tabella Di Conversione'>
				<IconButton
					size="large"
					sx={{ position: "absolute" }}
					onClick={() => setDrawerOpen(true)}
				>
					<MenuIcon fontSize='medium' />
				</IconButton>
			</Header>

			<Drawer anchor="left" open={drawerOpen} onClose={() => setDrawerOpen(false)}>
				<Box sx={{ width: 250, paddingTop: 10 }}>
					<List component="nav">
						<ListItemButton selected={true}>
							<ListItemIcon>
								<InboxIcon />
							</ListItemIcon>
							<Link href="index.html" color="inherit" underline='none'>Index</Link>
						</ListItemButton>
						<ListItemButton>
							<ListItemIcon>
								<SettingsIcon />
							</ListItemIcon>
							<Link href="settings.html" color="inherit" underline='none'>Settings</Link>
						</ListItemButton>
						<ListItemButton>
							<ListItemIcon>
								<ArticleIcon />
							</ListItemIcon>
							<Link href="log.html" color="inherit" underline='none'>Logs</Link>

						</ListItemButton>
					</List>
				</Box>
			</Drawer>

			<Container maxWidth="md" sx={{ py: 20 }}>
				<SerieTable api={api} />
			</Container>

			<Footer content={version ? "Ver. " + version : <Skeleton width="80px" />} />

		</ThemeProvider>
	);
}

function SerieTable({ api }: { api: API }) {

	const [data, setData] = useState([] as SerieTableEntry[]);

	useEffect(() => {
		api.getTable().then(res => setData(res));
	}, [])

	return (<>
		{data.map((serie, index) => (
			<Accordion key={index} component="details">
				<AccordionSummary component="summary">
					<Typography>{serie.title}</Typography>
				</AccordionSummary>
				<Divider />
				<AccordionDetails>
					<SeasonTabs api={api} season={serie.seasons} />
				</AccordionDetails>
			</Accordion>
		))}
	</>);
}


function SeasonTabs({ api, season }: { api: API, season: SeasonsTableEntry }) {
	const [tab, setTab] = useState(0);

	return (<>
		<Tabs value={tab} onChange={(_, val) => setTab(val)} aria-label="basic tabs example">
			{Object.entries(season).map(([key, _]) => (
				<Tab label={key} key={key}/>
			))}
		</Tabs>
		{Object.values(season)[tab].map((val:string) => (
			<Link href="#" color="inherit" key={val}>{val}</Link>
		))}
	</>);
}