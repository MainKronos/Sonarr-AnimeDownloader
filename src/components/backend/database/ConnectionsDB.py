import pathlib
from .Database import Database

from typing import Any, Generator, Union, Optional

class ConnectionsDB(Database):
	"""Gestisce il database delle Connections."""

	def __init__(self, db: pathlib.Path, scripts: pathlib.Path) -> None:
		"""
		Collega il database.

		Args:
		  db: il file del database
		  scripts: cartella contenente tutti gli scripts
		"""
		super().__init__(db)

		if not scripts.is_dir():
			raise NotADirectoryError(scripts)
		
		self.scripts = scripts

	def __len__(self):
		"""Numero di Connection presenti nel db."""
		return len(self._data)
	
	def __iter__(self) -> Generator[Any, Any, None]:
		for connection in self._data:
			yield connection
	
	def __get(self, key:str) -> Optional[dict[str, Any]]:
		"""
		Ritorna il dizionario con tutte le informazioni della Connection.

		Args:
		  key: Nome della Connection

		Returns:
		  La Connection
		"""
		for connection in self._data:
			if connection["name"] == key:
				return connection
		
		return None

	def __contains__(self, key: str) -> bool:
		"""
		Controlla se una tag esiste.

		Args:
		  key: Nome della Connection

		Returns:
		  True se il nome esiste altrimenti False.
		"""
		return self.__get(key) is not None
	
	def __getitem__(self, key:str) -> dict[str, Any]:
		"""
		Ritorna il dizionario con tutte le informazioni della Connection.

		Args:
		  key: Nome della Connection

		Returns:
		  La Connection
		"""

		value = self.__get(key)
		if value is None: raise KeyError(key)
		return value
	
	def __delitem__(self, key:str) -> None:
		"""
		Rimuove una Connection.
		
		Args:
		  key: nome della Connection
		"""

		connection = self[key]
		self._data.remove(connection)
		self.sync()
	
	def append(self, name:str, script:str, active:bool=False) -> None:
		"""
		Aggiunge un nuovo tag.

		Args:
		  name: nome della Connection
		  script: file bash della Connection
		  active: stato della Connection
		"""

		if name in self:
			raise ValueError(f"Nome {name} già presente.")
		
		if not script.endswith('.sh'):
			raise ValueError(f"Il file {script} non è un file bash.")
		
		if not self.scripts.joinpath(script).is_file():
			raise FileNotFoundError(self.scripts.joinpath(script))

		self._data.append({
			"name": name,
			"script": script,
			"active": active
		})
		self.sync()
	
	def isActive(self, name:str) -> bool:
		"""
		Controlla se una Connection è attiva.

		Args:
		  name: nome della connection

		Returns:
		  True se attiva / False se non attiva.
		"""

		connection = self[name]
		return connection["active"]
	
	def getPath(self, name:str) -> pathlib.Path:
		"""
		Ottiene il file dello script.

		Args:
		  name: nome della connection
		
		Returns:
		  Il file.
		"""

		connection = self[name]
		return self.scripts.joinpath(connection["script"]).absolute()
	
	def enable(self, name:str):
		"""
		Attiva una Connection.
		
		Args:
		  name: nome della connection
		"""

		connection = self[name]

		connection['active'] = True
		self.sync()

	def disable(self, name:str):
		"""
		Disattiva una Connection.
		
		Args:
		  name: nome della connection
		"""

		connection = self[name]

		connection['active'] = False
		self.sync()
	
	def toggle(self, name:str) -> bool:
		"""
		Cambia lo stato della Connection.
		
		Args:
		  name: nome della connection
		
		Returns:
		  Lo stato della Connections.
		"""
		connection = self[name]

		connection['active'] = not connection['active']
		self.sync()
		return connection['active']

	def fix(self) -> None:
		if not self.db.exists() or self.db.stat().st_size == 0:
			self.write([])