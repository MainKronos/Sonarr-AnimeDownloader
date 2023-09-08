import pathlib
import json

class Database:
	"""Gestione file JSON"""

	def __init__(self, db:pathlib.Path) -> None:
		"""
		Collega il database.

		Args:
		  db: il file del database
		"""
		if not db.is_file(): raise FileNotFoundError()
		self.db = db
		self.fix()
		self._data = self.read()
	
	def read(self):
		"""Legge le informazioni contenute nel database."""
		with self.db.open('r') as f:
			return json.load(f)
	
	def write(self, data) -> None:
		"""Scrive le informazioni nel database."""
		with self.db.open('w') as f:
			json.dump(data,f)
	
	def sync(self) -> None:
		"""Sincronizza il contenuto del db con quello in memoria."""
		self.write(self._data)

	def fix(self) -> None:
		"""Controlla l'integrità del database e nel caso lo corregge."""
		raise NotImplementedError()