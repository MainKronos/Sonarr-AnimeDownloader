from .Database import Database

from typing import Union, Any, Generator, Optional

class Tags(Database):

	def __get(self, key:Union[str, int]) -> Optional[dict[str, Any]]:
		"""
		Ritorna il dizionario con tutte le informazioni del Tag.

		Args:
		  key: nome | id del tag

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
		
		return None

	def __getitem__(self, key:Union[str, int]) -> dict[str, Any]:
		"""
		Ritorna il dizionario con tutte le informazioni del Tag.

		Args:
		  key: nome | id del tag

		Returns:
		  Il Tag.
		"""

		value = self.__get(key)
		if value is None: raise KeyError(key)
		return value
	
	def isActive(self, key: Union[str, int]) -> bool:
		"""
		Ritorna lo stato (attivo o non) di un tag.
		
		Args:
		  key: nome | id del tag

		Returns:
		  True se attivo / False se non attivo.
		"""

		tag = self[key]
		return tag['active']

	def enable(self, key: Union[str, int]):
		"""
		Attiva un tag.
		
		Args:
		  key: nome | id del tag
		"""

		tag = self[key]

		tag['active'] = True
		self.sync()

	def disable(self, key: Union[str, int]):
		"""
		Disattiva un tag.
		
		Args:
		  key: nome | id del tag
		"""

		tag = self[key]

		tag['active'] = False
		self.sync()

	def toggle(self, key: Union[str, int]) -> bool:
		"""
		Cambia lo stato del tag.
		
		Args:
		  key: nome | id del tag
		
		Returns:
		  Lo stato del tag.
		"""

		tag = self[key]

		tag['active'] = not tag['active']
		self.sync()
		return tag['active']

	def __delitem__(self, key: Union[str, int]) -> None:
		"""
		Rimuove un tag.
		
		Args:
		  key: nome | id del tag
		"""

		tag = self[key]
		self._data.remove(tag)
		self.sync()	
	
	def __contains__(self, key: Union[str, int]) -> bool:
		"""
		Controlla se una tag esiste.

		Args:
		  key: Nome | id del tag

		Returns:
		  True se l'id o il nome esiste altrimenti False.
		"""
		return self.__get(key) is not None
	
	def __len__(self) -> int:
		"""Numero di tag presenti nel db."""
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