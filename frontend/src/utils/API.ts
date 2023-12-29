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

    async putWekeup(): Promise<ResponseMsg> {
        const res = await fetch(encodeURI(this.backend + '/wekeup'), {
            method: "PUT"
        });
        return await res.json();
    }

    async getSettings(): Promise<SettingsOptions> {
        const res = await fetch(this.backend + '/settings');
        return await res.json();
    }

    async editSettings(setting:"AutoBind"|"LogLevel"|"MoveEp"|"RenameEp"|"ScanDelay"|"TagsMode", value:any): Promise<ResponseMsg>{
        const res = await fetch(encodeURI(this.backend + `/settings/${setting}`), {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ value: value })
        });
        return await res.json();
    }

    async getTable(): Promise<SerieTableEntry[]> {
        const res = await fetch(this.backend + '/table/');
        return await res.json();
    }

    async addSerie(title: string, absolute: boolean = false): Promise<ResponseMsg> {
        const res = await fetch(this.backend + '/table/', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ title: title, absolute: absolute })
        });
        return await res.json();
    }

    async deleteSerie(title: string): Promise<ResponseMsg> {
        const res = await fetch(encodeURI(this.backend + `/table/${title}`), {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        });
        return await res.json();
    }

    async editSerie(title: string, newTitle: string): Promise<ResponseMsg> {
        const res = await fetch(encodeURI(this.backend + `/table/${title}`), {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ title: newTitle })
        });
        return await res.json();
    }

    async addSeason(title: string, season: string): Promise<ResponseMsg> {
        const res = await fetch(encodeURI(this.backend + `/table/${title}`), {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ season: season })
        });
        return await res.json();
    }

    async deleteSeason(title: string, season: string): Promise<ResponseMsg> {
        const res = await fetch(encodeURI(this.backend + `/table/${title}/${season}`), {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        });
        return await res.json();
    }

    async editSeason(title: string, season: string, newSeason: string): Promise<ResponseMsg> {
        const res = await fetch(encodeURI(this.backend + `/table/${title}/${season}`), {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ season: newSeason })
        });
        return await res.json();
    }

    async addLinks(title: string, season: string, links: string[]): Promise<ResponseMsg> {
        const res = await fetch(encodeURI(this.backend + `/table/${title}/${season}`), {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ links: links })
        });
        return await res.json();
    }

    async deleteLink(title: string, season: string, link: string): Promise<ResponseMsg> {
        const res = await fetch(encodeURI(this.backend + `/table/${title}/${season}/${link}`), {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }
        });
        return await res.json()
    }

    async editLink(title: string, season: string, link: string, newLink: string): Promise<ResponseMsg> {
        const res = await fetch(encodeURI(this.backend + `/table/${title}/${season}/${link}`), {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ link: newLink })
        });
        return await res.json();
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

export interface ResponseMsg {
    message: string
}

export interface SettingsOptions { 
    AutoBind: boolean,
    LogLevel: "DEBUG" | "INFO" | "WARNING" | "ERROR" | "CRITICAL", 
    MoveEp: boolean,
    RenameEp: boolean,
    ScanDelay: number,
    TagsMode: "BLACKLIST" | "WHITELIST"
}