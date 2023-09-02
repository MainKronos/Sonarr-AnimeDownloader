from .Database import Database

from typing import Union, Any

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
			for tag in self.__data:
				if tag["id"] == key:
					return tag
		elif isinstance(key, str):
			# Ricerca per nome
			for tag in self.__data:
				if tag["name"] == key:
					return tag
		else:
			raise TypeError(str(type(key)))

	def __getitem__(self, key: Union[str, int]) -> bool:
		"""Ritorna lo stato (attivo o non) di un tag."""

		tag = self.__get(key)
		if tag is None: raise KeyError(key)

		return tag['active']
	
	def __delitem__(self, key: Union[str, int]) -> None:
		"""Rimuove un tag."""

		tag = self.__get(key)
		if tag is None: raise KeyError(key)

		self.__data.remove(tag)
		self.sync()
	
	def __setitem__(self, key: Union[str, int], value:bool) -> None:
		"""Attiva o disattiva un tag."""

		tag = self.__get(key)
		if tag is None: raise KeyError(key)

		tag['active'] = value
		self.sync()
	
	def __contains__(self, key: Union[str, int]) -> bool:
		"""Controlla se una tag esiste."""
		return self.__get(key) is not None
	
	def __len__(self) -> int:
		return len(self.__data)
	
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
		
		self.__data.append({
			"id": id,
			"name": name,
			"active": active
		})
		self.sync()
	
	def fix(self) -> None:
		if not self.db.exists() or self.db.stat().st_size == 0:
			self.write([])