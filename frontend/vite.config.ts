import { defineConfig } from 'vite'
import { resolve } from 'path'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({mode}) => {return{
	plugins: [react()],
	base: './',
	build: {
		outDir: 'build',
		rollupOptions: {
			input: {
				index: resolve(__dirname, 'index.html'),
				log: resolve(__dirname, 'log.html'),
				settings: resolve(__dirname, 'settings.html'),
			}
		},
	},
	resolve: {
		alias: {
			'@': resolve(__dirname, 'src'),
		}
	},
	define: {
		BACKEND: JSON.stringify(mode=='development' ? 'http://localhost:5000' : './')
	}
}})
