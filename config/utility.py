from typing import Dict, List

import json
import os

def readSettings() -> Dict[str, str]:
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

	json_location = "json/settings.json"
	update_fix = False

	settings = {}

	if os.path.exists(json_location):
		with open(json_location, 'r') as f:
			settings = json.loads(f.read())

		for info in data:
			if info not in settings:
				settings[info] = data[info]
				update_fix = True
	else:
		settings = data
		update_fix = True

	if update_fix:
		with open(json_location, 'w') as f:
			f.write(json.dumps(settings, indent='\t'))
	
	return settings

class Table:
	file = "json/table.json"
	
	@classmethod
	@property
	def data(self) -> List[Dict]:
		"""
		Lista di dizionari contenente tutta la tabella di conversione.
		"""
		if not os.path.exists(self.file):
			self.__write([])
			return []


		with open(self.file, 'r') as f:
			return json.loads(f.read())
	
	@classmethod
	def append(self, data: Dict):
		"""
		Aggiunge un nuovo anime ho delle informazioni.
		"""
		table = self.data


		for anime in table:
			if data["title"] == anime["title"]: # Se esiste già l'anime nella tabella
				if data["season"] in anime["seasons"]: # Se esiste già la stagione
					for link in data["links"]:
						if link not in anime["seasons"][data["season"]]: # Se il link non è già presente
							anime["seasons"][data["season"]].append(link)  # aggiunge un'altro link
				else:
					if not anime["absolute"] and not data["absolute"]:  # Se la numerazione non è assoluta
						anime["seasons"][data["season"]] = list(data["links"]) # inizializza una nuova stagione

				break
		else: # se non è stato trovato nessun anime
			table.append({
				"title": data["title"],
				"seasons": {data["season"]: data["links"]},
				"absolute": data["absolute"]
			})

		table.sort(key=lambda s: s["title"])
		self.__write(table)
	
	@classmethod
	def __write(self, table:List):
		"""
		Svrascrive la tabella con le nuove informazioni.
		"""
		with open(self.file, 'w') as f:
			f.write(json.dumps(table, indent=4))