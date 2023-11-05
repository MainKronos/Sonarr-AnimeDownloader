import { ReactNode } from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

interface HeaderProps {
	title: string,
	children?: ReactNode
}

export function Header({ title, children }: HeaderProps) {
	return (
		<AppBar position="fixed">
			<Toolbar sx={{ padding: "20px" }}>
				{children}

				<Typography variant="h4" textAlign='center' sx={{ flex: 1, fontWeight: 500 }} component="h1">
					{title}
				</Typography>

			</Toolbar>
		</AppBar>
	);
};