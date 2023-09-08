import pathlib
from .Database import Database

from typing import Union, Any, Generator

class Table(Database):
	def sync(self) -> None:
		self._data.sort(key=lambda s: s["title"])
		return super().sync()

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
	
	def __contains__(self, key: str) -> bool:
		"""Controlla se una serie esiste."""
		return self.__get(key) is not None

	def isAbsolute(self, title) -> bool:
		"""Ritorna True se la serie è in formato absolute."""
		return self[title]["absolute"]
	
	### REMOVE

	def removeSerie(self, title:str) -> None:
		"""
		Rimuove una serie.

		Args:
		  title: il titolo della serie
		"""

		serie = self[title]
		self._data.remove(serie)
		self.sync()
	
	def removeSeason(self, title:str, season:Union[str,int]) -> None:
		"""
		Rimuove una stagione.

		Args:
		  title: il titolo della serie
		  season: il numero della stagione (può essere anche 'absolute' come numero)
		"""

		# Per sicurezza
		season = str(season)

		serie = self[title]
		serie["seasons"].pop(season)
		self.sync()

	def removeUrl(self, title:str, season:Union[str,int], url:str) -> None:
		"""
		Rimuove un url di download.

		Args:
		  title: il titolo della serie
		  season: il numero della stagione (può essere anche 'absolute' come numero)
		  url: l'url di download
		"""

		# Per sicurezza
		season = str(season)

		serie = self[title]
		s = serie["seasons"][season]
		s.remove(url)
		self.sync()

	### APPEND

	def appendSerie(self, title:str, absolute:bool=False) -> bool:
		"""
		Aggiunge una nuova serie alla tabella.

		Args:
		  title: titolo della serie
		  absolute: se è in formato assoluto
		
		Returns:
		  True se è stata aggiunta, False altrimenti
		"""

		# Controllo se c'è già una serie con quel titolo
		if title in self: return False

		# Aggiungo la serie
		self._data.append({
			"title": title,
			"absolute": absolute,
			"seasons": {}
		})
		self.sync()
		return True
	
	def appendSeason(self, title:str, season:Union[str,int]) -> bool:
		"""
		Aggiunge una nuova stagione alla serie, se la serie non esiste la crea.

		Args:
		  title: titolo della serie
		  season: il numero della stagione (può essere anche 'absolute' come numero)
		
		Returns:
		  True se è stata aggiunta, False altrimenti
		"""

		# Controllo se c'è una serie con quel titolo
		if title not in self:
			# Altrimenti la creo
			if not self.appendSerie(title):
				return False

		serie = self[title]

		# Se la serie è in formato assoluto e la stagione non si chiama "absolute"
		# Oppure la serie non è in formato assoluto e la stagione si chiama "absolute"
		if (serie["absolute"]) ^ (season == "absolute"): return False

		# Se è già presente una stagione con uno stesso numero
		if season in serie["seasons"]: return False

		# Aggiungo la stagione
		serie["seasons"][season] = []
		self.sync()
		return True
	
	def appendUrls(self, title:str, season:Union[str,int], urls:list[str]) -> bool:
		"""
		Aggiunge un nuovo url alla stagione, se la stagione non esiste la crea, se la serie non esiste la crea.

		Args:
		  title: titolo della serie
		  season: il numero della stagione (può essere anche 'absolute' come numero)
		  urls: gli url di download
		
		Returns:
		  True se è stata aggiunta, False altrimenti
		"""

		# Controllo se c'è una serie con quel titolo
		if title not in self:
			# Altrimenti la creo
			if not self.appendSerie(title):
				return False

		serie = self[title]

		# Controllo se c'è una stagione con quel numero
		if season not in serie["seasons"]:
			# Altrimenti la creo
			if not self.appendSeason(title, season):
				return False

		# Controllo se c'è gia lo stesso url
		urls = list(filter(lambda x: x not in serie["seasons"][season], urls))
		if len(urls) == 0: return False

		# Aggiungo il nuovo url
		serie["seasons"][season].extend(urls)
		self.sync()
		return True
	
	### RENAME

	def renameSerie(self, title:str, new_title:str) -> None:
		"""
		Rinomina una serie.

		Args:
		  title: il titolo della serie
		  new_title: il nuovo titolo
		"""

		# Controllo se c'è già un titolo `new_title`:
		if new_title in self: return False

		serie = self[title]
		serie["title"] = new_title
		self.sync()
	
	def renameSeason(self, title:str, season:Union[str,int], new_season:Union[str,int]) -> None:
		"""
		Rinomina una stagione.

		Args:
		  title: il titolo della serie
		  season: il numero della stagione (può essere anche 'absolute' come numero)
		  new_season: il nuovo numero della stagione (può essere anche 'absolute' come numero)
		"""

		# Per sicurezza
		season = str(season)
		new_season = str(new_season)

		serie = self[title]

		# Controllo se c'è gia la stagione `new_season`
		if new_season in serie["seasons"]: return False

		old = serie["seasons"].pop(season)
		serie["seasons"][new_season] = old
		self.sync()

	def renameUrl(self, title:str, season:Union[str,int], url:str, new_url:str) -> None:
		"""
		Rimuove un url di download.

		Args:
		  title: il titolo della serie
		  season: il numero della stagione (può essere anche 'absolute' come numero)
		  url: l'url di download
		  new_url: il nuovo url di download
		"""

		# Per sicurezza
		season = str(season)

		serie = self[title]
		s = serie["seasons"][season]

		# Controllo che non ci sia già un url uguale
		if new_url in s: return False

		index = s.index(url)
		s[index] = new_url
		self.sync()