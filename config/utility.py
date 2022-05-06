from typing import Dict, List, Optional, Union

import json
import os
import requests

class classproperty(object):
	def __init__(self, fget):
		self.fget = fget
	def __get__(self, owner_self, owner_cls):
		return self.fget(owner_cls)

class Settings:
	file = "json/settings.json"

	@classproperty
	def data(self) -> Dict[str,str]:
		"""
		Legge le impostazione dal file `json/settings.json`.

		```
		return {
			"LogLevel": "DEBUG",
			"RenameEp": True,
			"MoveEp": True,
			"ScanDelay": 30,
			"AutoBind": False
		}
		```
		"""

		data = {
			"LogLevel": "DEBUG",
			"RenameEp": True,
			"MoveEp": True,
			"ScanDelay": 30,
			"AutoBind": False
		}

		update_fix = False

		settings = {}

		if os.path.exists(self.file):
			with open(self.file, 'r') as f:
				settings = json.loads(f.read())

			for info in data:
				if info not in settings:
					settings[info] = data[info]
					update_fix = True

			if settings["ScanDelay"] < 30 : settings["ScanDelay"] = 30

		else:
			settings = data
			update_fix = True

		if update_fix:
			self.write(settings)
		
		return settings

	@classmethod
	def update(self, AutoBind:Optional[bool], LogLevel:Optional[str], MoveEp:Optional[bool], RenameEp:Optional[bool], ScanDelay:Optional[int]) -> str:
		settings = self.data

		log = "Nessuna modifica avvenuta." # messaggio

		if AutoBind is not None:
			settings["AutoBind"] = AutoBind
			log = "Auto Ricerca Link aggiornato."
		if LogLevel is not None:
			settings["LogLevel"] = LogLevel
			log = "Livello del Log aggiornato."
		if MoveEp is not None:
			settings["MoveEp"] = MoveEp
			log = "Sposta Episodi aggiornato."
		if RenameEp is not None:
			settings["RenameEp"] = RenameEp
			log = "Rinomina Episodi aggiornato."
		if ScanDelay is not None:
			settings["ScanDelay"] = ScanDelay
			log = "Intervallo Scan aggiornato."

		self.write(settings)

		return log
	
	@classmethod
	def isValid(self, settings:Dict[str,str]) -> bool:
		"""
		Controlla se le informazioni sono valide.
		"""

		if "AutoBind" not in settings: return False
		if "LogLevel" not in settings: return False
		if "MoveEp" not in settings: return False
		if "RenameEp" not in settings: return False
		if "ScanDelay" not in settings: return False

		return True


	@classmethod
	def write(self, data:Dict[str,str]):
		"""
		Sovrascrive le impostazioni con le nuove informazioni.
		"""
		if self.isValid(data):
			with open(self.file, 'w') as f:
				f.write(json.dumps(data, indent=4))


class Table:
	file = "json/table.json"
	
	@classproperty
	def data(self) -> List[Dict]:
		"""
		Lista di dizionari contenente tutta la tabella di conversione.
		"""
		if not os.path.exists(self.file):
			self.write([])
			return []


		with open(self.file, 'r') as f:
			return json.loads(f.read())
	
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


