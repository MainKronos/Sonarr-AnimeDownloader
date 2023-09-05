from .Database import Database

from typing import Union, Any, Generator

class Table(Database):
	def fix(self) -> None:
		if not self.db.exists() or self.db.stat().st_size == 0:
			self.write([])
	
	def __iter__(self) -> Generator[Any, Any, None]:
		for serie in self._data:
			yield serie
	
	def __len__(self) -> int:
		return len(self._data)
	
	def __get(self, key:str) -> dict:
		"""
		Ritorna la serie con il titolo richiesto.

		Args:
		  key: il titolo della serie
		
		Returns:
		  La serie
		"""

		for serie in self._data:
			if serie["title"] == key:
				return serie
	
	def __getitem__(self, key:str) -> dict:
		"""
		Ritorna la serie con il titolo richiesto.

		Args:
		  key: il titolo della serie
		
		Returns:
		  La serie
		"""

		serie = self.__get(key)
		if serie is None: raise KeyError(key)
		return serie
	
	def __delitem__(self, key:str) -> None:
		"Rimuove una serie."

		serie = self[key]
		self._data.remove(serie)
		self.sync()
	
	def __contains__(self, key: str) -> bool:
		"""Controlla se una serie esiste."""
		return self.__get(key) is not None

	def isAbsolute(self, title) -> bool:
		"""Ritorna True se la serie è in formato absolute."""
		return self[title]["absolute"]