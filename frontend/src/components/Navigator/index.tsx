import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';

import SettingsIcon from '@mui/icons-material/Settings';
import InboxIcon from '@mui/icons-material/Inbox';
import ArticleIcon from '@mui/icons-material/Article';


interface NavigatorProps {
	drawerState: boolean,
	setDrawerState: (state:boolean) => void,
}

export function Navigator({drawerState, setDrawerState}:NavigatorProps) {

	function closeDrawer() {setDrawerState(false)}

	return (
		<Drawer anchor="left" open={drawerState} onClose={(closeDrawer)}>
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
	)
}