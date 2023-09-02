from .Database import Database

class Settings(Database):
	def __getitem__(self, key: str):
		return self._data[key]
	
	def __setitem__(self, key: str, value):
		if key not in self._data: raise KeyError(key)

		self._data[key] = value
		self.sync()
	
	def fix(self) -> None:
		if not self.db.exists() or self.db.stat().st_size == 0: 
			self.write({
				"AutoBind": True,
				"LogLevel": "DEBUG",
				"MoveEp": True,
				"RenameEp": True,
				"ScanDelay": 30,
				"TagsMode": "WHITELIST"
			})