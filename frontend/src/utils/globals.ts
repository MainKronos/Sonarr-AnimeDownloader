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