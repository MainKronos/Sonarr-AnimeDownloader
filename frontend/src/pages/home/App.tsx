// import * from "react";
import { useState, useEffect } from 'react';

import { Header, Footer, Navigator } from '@/components';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import IconButton from '@mui/material/IconButton';

import Container from '@mui/material/Container';
import Skeleton from '@mui/material/Skeleton';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Divider from '@mui/material/Divider';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';


import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';

import MenuIcon from '@mui/icons-material/Menu';
import MovieIcon from '@mui/icons-material/Movie';
import AddIcon from '@mui/icons-material/Add';
import DownloadIcon from '@mui/icons-material/Download';
import UploadIcon from '@mui/icons-material/Upload';

import { API } from '@/utils/API';
import { theme } from '@/utils/globals'
import type { SerieTableEntry, SeasonsTableEntry } from '@/utils/types';

export default function App() {

	const [drawerState, setDrawerState] = useState(false);
	const [version, setVersion] = useState('');

	function openDrawer() { setDrawerState(true) }

	const api = new API('http://127.0.0.1:5000');

	useEffect(() => {
		api.getVersion().then(res => setVersion(res));
	}, []);

	return (
		<ThemeProvider theme={theme}>
			<CssBaseline />

			<Header title='Tabella Di Conversione'>
				<IconButton
					size="large"
					sx={{ position: "absolute" }}
					onClick={openDrawer}
				>
					<MenuIcon fontSize='medium' />
				</IconButton>
			</Header>

			<Navigator drawerState={drawerState} setDrawerState={setDrawerState} />

			<SerieTable api={api} />

			<Footer content={version ? "Ver. " + version : <Skeleton width="80px" />} />

		</ThemeProvider>
	);
}

function SerieTable({ api }: { api: API }) {

	const [data, setData] = useState([] as SerieTableEntry[]);

	useEffect(() => {
		api.getTable().then(res => setData(res));
	}, [])

	return (
		<Container maxWidth="md" sx={{ py: 20 }}>
			<Paper>
				<Button aria-label="add" size="large" variant="text" fullWidth={true}>
					<AddIcon />
				</Button>
			</Paper>

			{data.map((serie, index) => (
				<Accordion key={index}>
					<AccordionSummary expandIcon={<MovieIcon />}>
						<Typography>{serie.title}</Typography> {serie.absolute && <Chip label="absolute" color="primary" size="small"/>}
					</AccordionSummary>
					<Divider />
					<AccordionDetails>
						<SeasonTabs api={api} season={serie.seasons} />
					</AccordionDetails>
				</Accordion>
			))}

			<Paper>
				<Stack direction="row" >
					<Button aria-label="download" size="large" variant="text" fullWidth={true}>
						<DownloadIcon />
					</Button>
					<Button aria-label="upload" size="large" variant="text" fullWidth={true}>
						<UploadIcon />
					</Button>
				</Stack>
			</Paper>

		</Container>
	);
}


function SeasonTabs({ api, season }: { api: API, season: SeasonsTableEntry }) {
	const [tab, setTab] = useState(0);

	return (<>
		<Tabs value={tab} onChange={(_, val) => val && setTab(val)} aria-label="basic tabs example">
			{Object.entries(season).map(([key, _]) => (
				<Tab label={key} key={key} />
			))}
			<Tab icon={<AddIcon />} aria-label="add" value={null}/>
		</Tabs>
		<List dense={true}>
			{Object.values(season)[tab].map((val: string) => (
				<ListItem key={val}>
					<ListItemButton component="a" href={val} target="_blank">
						<ListItemText primary={val} />
					</ListItemButton>
				</ListItem>
			))}
		</List>
	</>);
}