import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
	palette: {
		mode: 'dark',
		primary: {
			main: '#9FA8DA',
		},
		secondary: {
			main: '#9FA8DA',
		},
		text: {
			primary: 'rgba(255,255,255,0.6)',
		},
	},
	components: {
		MuiAccordionSummary: {
			styleOverrides: {
				root: {
					flexDirection: 'row-reverse',
				},
				content: {
					justifyContent: 'space-between'
				},
				expandIconWrapper: {
					marginRight: "10px",
					color: 'rgba(255,255,255,0.6)'
				},
			}
		},
		MuiTabs: {
			styleOverrides: {
				root: {
					borderBottom: '1px solid rgba(255, 255, 255, 0.12)',
				}
			}
		}
	}
});