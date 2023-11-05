export interface SerieTableEntry {
	title: string,
	absolute: boolean,
	seasons: SeasonsTableEntry
}

export interface SeasonsTableEntry {
	[season:string]: string[]
}