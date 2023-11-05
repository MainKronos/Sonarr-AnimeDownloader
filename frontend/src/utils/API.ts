import type {SerieTableEntry} from './types';

export class API {
	backend: string;
	constructor(backend:string) {
		this.backend = backend + '/api';
	}

	async getVersion():Promise<string>{
		const res = await fetch(this.backend + '/version');
		const data = await res.json()
		return data.version;
	}

	async getTable():Promise<SerieTableEntry[]>{
		const res = await fetch(this.backend + '/table');
		return await res.json()
	}
}