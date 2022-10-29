from typing import Dict, Optional
import os
import json

from utility.classproperty import classproperty

class Settings:
	file = "json/settings.json"
	tmp = None # variabile temporanea contenente le impostazioni, in caso di cambiamenti ritorna a None

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
			"AutoBind": False,
			"TagsMode": "BLACKLIST"
		}
		```
		"""

		if self.tmp is not None: return self.tmp

		data = {
			"LogLevel": "DEBUG",
			"RenameEp": True,
			"MoveEp": True,
			"ScanDelay": 30,
			"AutoBind": False,
			"TagsMode": "BLACKLIST"
		}

		update_fix = False

		settings = {}

		if os.path.exists(self.file) and os.path.getsize(self.file) > 0:
			try:
				with open(self.file, 'r') as f:
					settings = json.loads(f.read())

			except json.JSONDecodeError:
				settings = data
				update_fix = True

			else:
				for info in data:
					if info not in settings:
						settings[info] = data[info]
						update_fix = True

			if settings["ScanDelay"] < 30 : 
				settings["ScanDelay"] = data["ScanDelay"] # applico l'impostazione di default
				update_fix = True

			if settings["TagsMode"] not in ("BLACKLIST", "WHITELIST"): 
				settings["TagsMode"] = data["TagsMode"] # applico l'impostazione di default
				update_fix = True

		else:
			settings = data
			update_fix = True

		if update_fix:
			self.write(settings)
		
		self.tmp = settings
		
		return settings

	@classmethod
	def update(self, AutoBind:Optional[bool], LogLevel:Optional[str], MoveEp:Optional[bool], RenameEp:Optional[bool], ScanDelay:Optional[int], TagsMode:str) -> str:
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
		if TagsMode is not None:
			settings["TagsMode"] = TagsMode
			log = "Modalità tags aggiornata."

		self.write(settings)

		self.tmp = None # invalida il tmp
		self.refresh(self)
		return log
	
	@classmethod
	def refresh(self, silent=False):
		"""
		Aggiorna le impostazioni a livello globale.
		"""
		# Funzione inizializzata in main per problemi di circular import
		pass
	
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
		if "TagsMode" not in settings: return False

		return True


	@classmethod
	def write(self, data:Dict[str,str]):
		"""
		Sovrascrive le impostazioni con le nuove informazioni.
		"""
		if self.isValid(data):
			with open(self.file, 'w') as f:
				f.write(json.dumps(data, indent=4))
				return True
		else:
			return False
	
	