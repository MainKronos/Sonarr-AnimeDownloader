from .Database import Database

from typing import Literal

class Settings(Database):
	def __getitem__(self, key: Literal["AutoBind","LogLevel","MoveEp","RenameEp","ScanDelay","TagsMode","MaxConcurrentDownloads"]):
		return self._data[key]

	def __setitem__(self, key: Literal["AutoBind","LogLevel","MoveEp","RenameEp","ScanDelay","TagsMode","MaxConcurrentDownloads"], value):
		if key not in self._data: raise KeyError(key)

		self._data[key] = value
		self.sync()

	def fix(self) -> None:
		defaults = {
			"AutoBind": True,
			"LogLevel": "DEBUG",
			"MoveEp": True,
			"RenameEp": True,
			"ScanDelay": 30,
			"TagsMode": "WHITELIST",
			"MaxConcurrentDownloads": 10
		}

		if not self.db.exists() or self.db.stat().st_size == 0:
			self.write(defaults)
			return

		# Aggiunge eventuali nuove impostazioni mancanti (aggiornamento da una versione precedente)
		data = self.read()
		missing = {k: v for k, v in defaults.items() if k not in data}
		if missing:
			data.update(missing)
			self.write(data)
	
	def __iter__(self):
		for key in self._data:
			yield key
	
	def __len__(self) -> int:
		return len(self._data)
	
	def __contains__(self, key: str):
		"""Controlla se un impostazione esiste."""

		return key in self._data