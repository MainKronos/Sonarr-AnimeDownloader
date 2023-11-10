import { ReactNode } from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';

interface FooterProps {
	content:ReactNode
}

export function Footer({content}:FooterProps) {
	return (
		<Paper square elevation={1} sx={{ position: 'fixed', bottom: 0, left: 0, right: 0, padding: '16px', borderTop: '1px solid', borderColor: 'divider' }}>
			<Typography variant="body1" noWrap sx={{flex: 1, display: 'flex', justifyContent: 'center'}}>
				{content}
			</Typography>
		</Paper>
	);
};