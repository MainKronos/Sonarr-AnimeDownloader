export class API {
    backend: string;
    constructor(backend: string) {
        this.backend = backend + '/api';
    }

    async getVersion(): Promise<string> {
        const res = await fetch(this.backend + '/version');
        const data = await res.json()
        return data.version;
    }

    async getTable(): Promise<SerieTableEntry[]> {
        const res = await fetch(this.backend + '/table/');
        return await res.json()
    }

    async addSerie(title: string, absolute: boolean = false) {
        const res = await fetch(this.backend + '/table/', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ title: title, absolute: absolute })
        });
        return await res.json()
    }

    async deleteSerie(title: string) {
        const res = await fetch(encodeURI(this.backend + `/table/${title}`), {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        });
        return await res.json()
    }

    async editSerie(title: string, newTitle: string) {
        const res = await fetch(encodeURI(this.backend + `/table/${title}`), {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ title: newTitle })
        });
        return await res.json()
    }

    async addSeason(title: string, season: string) {
        const res = await fetch(encodeURI(this.backend + `/table/${title}`), {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ season: season })
        });
        return await res.json()
    }

    async deleteSeason(title: string, season: string) {
        const res = await fetch(encodeURI(this.backend + `/table/${title}/${season}`), {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        });
        return await res.json()
    }

    async editSeason(title: string, season: string, newSeason: string) {
        const res = await fetch(encodeURI(this.backend + `/table/${title}/${season}`), {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ season: newSeason })
        });
        return await res.json()
    }

    async addLinks(title: string, season: string, links: string[]) {
        const res = await fetch(encodeURI(this.backend + `/table/${title}/${season}`), {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ links: links })
        });
        return await res.json()
    }

    async deleteLink(title:string, season:string, link:string){
        const res = await fetch(encodeURI(this.backend + `/table/${title}/${season}/${link}`), {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        });
        return await res.json()
    }

    async editLink(title:string, season:string, link:string, newLink: string){
        const res = await fetch(encodeURI(this.backend + `/table/${title}/${season}/${link}`), {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ link: newLink })
        });
        return await res.json()
    }
}

export interface SerieTableEntry {
    title: string,
    absolute: boolean,
    seasons: SeasonsTableEntry
}

export interface SeasonsTableEntry {
    [season: string]: string[]
}