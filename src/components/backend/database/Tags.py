from .Database import Database

from typing import Union, Any, Generator

class Tags(Database):

	def __get(self, key:Union[str, int]) -> Union[dict[str, Any], None]:
		"""
		Ritorna il dizionario con tutte le informazioni del Tag.

		Args:
		  key: Nome | id del tag

		Returns:
		  Il Tag
		"""
		if isinstance(key, int):
			# Ricerca per id
			for tag in self._data:
				if tag["id"] == key:
					return tag
		elif isinstance(key, str):
			# Ricerca per nome
			for tag in self._data:
				if tag["name"] == key:
					return tag
		else:
			raise TypeError(str(type(key)))	

	def __getitem__(self, key:Union[str, int]) -> Union[dict[str, Any], None]:
		"""
		Ritorna il dizionario con tutte le informazioni del Tag.

		Args:
		  key: Nome | id del tag

		Returns:
		  Il Tag
		"""

		value = self.__get(key)
		if value is None: raise KeyError(key)
		return value
	
	def isActive(self, key: Union[str, int]) -> bool:
		"""Ritorna lo stato (attivo o non) di un tag."""

		tag = self[key]
		if tag is None: raise KeyError(key)

		return tag['active']

	def enable(self, key: Union[str, int]):
		"""Attiva un tag."""

		tag = self[key]
		if tag is None: raise KeyError(key)

		tag['active'] = True
		self.sync()

	def disable(self, key: Union[str, int]):
		"""Disattiva un tag."""

		tag = self[key]
		if tag is None: raise KeyError(key)

		tag['active'] = False
		self.sync()

	def __delitem__(self, key: Union[str, int]) -> None:
		"""Rimuove un tag."""

		tag = self[key]
		self._data.remove(tag)
		self.sync()	
	
	def __contains__(self, key: Union[str, int]) -> bool:
		"""Controlla se una tag esiste."""
		return self.__get(key) is not None
	
	def __len__(self) -> int:
		return len(self._data)
	
	def __iter__(self) -> Generator[Any, Any, None]:
		for tag in self._data:
			yield tag
	
	def append(self, id:int, name:str, active:bool=False) -> None:
		"""
		Aggiunge un nuovo tag.

		Args:
		  id: ID del tag
		  name: nome del tag
		  active: stato del tag
		"""

		if id in self:
			raise ValueError(f"ID {id} già presente")
		if name in self:
			raise ValueError(f"Nome '{name}' già presente")
		
		self._data.append({
			"id": id,
			"name": name,
			"active": active
		})
		self.sync()
	
	def fix(self) -> None:
		if not self.db.exists() or self.db.stat().st_size == 0:
			self.write([])