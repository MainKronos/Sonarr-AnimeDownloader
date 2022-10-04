from typing import Dict, List, Union
import os
import json

from .classproperty import classproperty

class Table:
	file = "json/table.json"
	
	@classproperty
	def data(self) -> List[Dict]:
		"""
		Lista di dizionari contenente tutta la tabella di conversione.
		"""
		if os.path.exists(self.file) and os.path.getsize(self.file) > 0:
			try:
				with open(self.file, 'r') as f:
					return json.loads(f.read())
			except json.JSONDecodeError:
				pass
		
		self.write([])
		return []
	
	@classmethod
	def append(self, data: Dict) -> str:
		"""
		Aggiunge un nuovo anime o delle informazioni.
		"""
		table = self.data

		log = "" # messaggio


		for anime in table:
			if data["title"] == anime["title"]: # Se esiste già l'anime nella tabella
				if data["season"] in anime["seasons"]: # Se esiste già la stagione
					for link in data["links"]:
						if link not in anime["seasons"][data["season"]]: # Se il link non è già presente
							anime["seasons"][data["season"]].append(link)  # aggiunge un'altro link
							log = "Nuovo link aggiunto."
						else:
							log = "Il link è già presente."
						break
					else:
						log = f"La stagione {data['season']} è già presente."
				else:
					if not anime["absolute"] and not data["absolute"]:  # Se la numerazione non è assoluta
						anime["seasons"][data["season"]] = list(data["links"]) # inizializza una nuova stagione
						log = f"Stagione {data['season']} di {data['title']} aggiunta."
					else:
						log = "Impossibile aggiungere una stagione se la numerazione è assoluta."
				break
		else: # se non è stato trovato nessun anime
			table.append({
				"title": data["title"],
				"seasons": {data["season"] if not data["absolute"] else "absolute": data["links"]},
				"absolute": data["absolute"]
			})
			log = f"{data['title']} aggiunto."

		table.sort(key=lambda s: s["title"])
		self.write(table)

		return log
	
	@classmethod
	def remove(self, title:str, season:str=None, link:str=None) -> str:
		"""
		Rimuove un anime o delle informazioni.
		"""

		table = self.data

		log = "" # messaggio

		for anime in table:
			if anime["title"] == title:
				if not (season or link):
					table.remove(anime)
					log = f"{title} rimosso."
					break
				else:
					for seasonIndex in anime["seasons"]:
						if seasonIndex == str(season):
							if not link:
								anime["seasons"].pop(seasonIndex)
								log = f"Stagione {season} di {title} rimossa."
								break
							else:
								for url in anime["seasons"][seasonIndex]:
									if url == link:
										anime["seasons"][seasonIndex].remove(url)
										log = "Link rimosso."
										break
								else:
									log = "Link inesistente."
								break
					else:
						log = f"Stagione {season} di {title} inesistente."
					break
		else:
			log = f"{title} inesistente."

		self.write(table)
		return log
	
	@classmethod
	def edit(self, title:Union[str,list], season:Union[str,list]=None, link:list=None) -> str:
		"""
		modifica un anime o delle informazioni.
		"""

		table = self.data

		edit = None # valore da editare

		log = "" # messaggio

		for anime in table:
			if isinstance(title, list):
				if anime["title"] == title[0]:
					anime["title"] = title[1]
					log = f"{title[0]} modificato."
					break
			else:
				if anime["title"] == title:
					for seasonIndex in anime["seasons"]:
						if isinstance(season, list):
							if seasonIndex == str(season[0]):
								anime["seasons"][season[1]] = anime["seasons"].pop(seasonIndex)
								anime["absolute"] = False
								log = f"Stagione {season[0]} di {title} modificata."
								break
						else:
							for index, url in enumerate(anime["seasons"][seasonIndex]):
								if url == link[0]:
									anime["seasons"][seasonIndex][index] = link[1]
									log = "Link modificato."
									break
							else:
								log = "Link inesistente."
							break
					else:
						log = f"Stagione {season[0] if isinstance(season, list) else season} di {title} inesistente."
					break
		else:
			log = f"{title[0] if isinstance(title, list) else title} inesistente."

		self.write(table)
		return log
	
	@classmethod
	def isValid(self, table:List) -> bool:
		"""
		Controlla se le informazioni sono valide.
		"""
		for anime in table:
			if "absolute" not in anime: return False
			if "seasons" not in anime: return False
			if "title" not in anime: return False
		
		return True

	@classmethod
	def write(self, table:List):
		"""
		Sovrascrive la tabella con le nuove informazioni.
		"""
		if self.isValid(table):
			with open(self.file, 'w') as f:
				f.write(json.dumps(table, indent=4))

				return True
		else:
			return False