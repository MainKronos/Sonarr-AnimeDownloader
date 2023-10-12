export class API {
	backend: string;
	constructor(backend:URL) {
		this.backend = backend.origin + '/api';
	}

	async getVersion():Promise<string>{
		const res = await fetch(this.backend + '/version');
		const data = await res.json()
		return data.version;
	}

	async getTable():Promise<any[]>{
		const res = await fetch(this.backend + '/table');
		return await res.json()
	}
}