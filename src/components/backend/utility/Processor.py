from ..core import Constant as ctx
from ..connection import Sonarr
from ..database import *

import logging
import functools

class Processor:
	"""Processa i dati che provengono da Sonarr"""

	def __init__(self, sonarr:Sonarr, *, settings:Settings=None, tags:Tags=None, table:Table=None) -> None:
		self.sonarr = sonarr
		self.settings = settings
		self.tags = tags
		self.table = table
		self.log = ctx.LOGGER
	
	def getData(self) -> list:
		"""Restituisce i dati elaborati."""

		missing = self.getAllMissing()

		missing = functools.reduce(self.__reduce, missing, [])

		missing = map(self.__bindUrl, missing)

		return list(missing)

	def getAllMissing(self) -> list:
		"""
		Ottiene tutta la lista di episodi mancanti con la formattazione fornita da Sonarr.
		
		Returns:
		  La lista di episodi mancanti.
		"""

		missing = []

		for page in range(1,50):
			res = self.sonarr.wantedMissing(page=page)
			res.raise_for_status()
			res = res.json()

			if len(res["records"]) == 0: break

			missing.extend(filter(self.__filter, res['records']))

		return missing


	def __filter(self, elem:dict) -> bool:
		"""
		Filtra gli episodi non richiesti.

		Args:
		  elem: elemento da filtrare
		
		Returns:
		  True da prendere / False da scartare
		"""

		# Controllo che sia effettivamente un anime
		if elem["series"]["seriesType"] != 'anime': return False

		# Controllo i tag
		tag_active = any([self.tags.isActive(x) for x in elem["series"]["tags"] if x in self.tags])
		if tag_active and self.settings["TagsMode"] == "BLACKLIST" or not tag_active and self.settings["TagsMode"] == "WHITELIST": return False

		return True

	def __reduce(self, base:list, elem:dict):
		"""
		Riduce le informazioni della lista di episodi in informazioni essenziali.

		Args:
		  base: lista contenente il risultato della riduzione
		  elem: elemento da aggiungere alla base
		"""
		
		# Controllo se è presentè già la serie
		serie = self.__extractSerie(elem)
		for s in base:
			if s["id"] == serie["id"]:
				# Se esiste la salvo
				serie = s
				break
		else:
			# altrimenti l'aggiungo
			base.append(serie)
			serie["seasons"] = []
		
		# Controllo se è già presente la stagione
		season = self.__extractSeason(elem)
		for s in serie["seasons"]:
			if s["number"] == season["number"]:
				# Se esiste la salvo
				season = s
				break
		else:
			# altrimenti l'aggiungo
			serie["seasons"].append(season)
			season["episodes"] = []

		# Aggiungom l'episodio
		episode = self.__extractEpisode(elem)
		season["episodes"].append(episode)

		return base
	
	def __bindUrl(self, elem:dict) -> dict:
		"""
		Collega l'url di download a tutte le stagioni contenute nella serie in elem.

		Args:
		  elem: serie che contiene le stagioni a cui verranno aggiunti gli url di download

		Returns:
		  La serie con gli url aggiunti.
		"""
		title = elem["title"]
		if title not in self.table: return False

		table_entry = self.table[title]

		if table_entry["absolute"]:
			self.__convertToAbsolute(elem)
			elem["seasons"][0]["urls"] = table_entry["seasons"]["absolute"]
			return elem
		else:
			pass
			# TODO: da completare il caso normale
	
	def __convertToAbsolute(self, elem:dict) -> dict:
		"""
		Converte una serie normale in una con formato 'absolute', cioè con una sola stagione di nome absolute.

		Args:
		  elem: la serie da convertire.
		
		Returns:
		  La serie converita.
		"""
		absolute_season = elem["seasons"][0]
		absolute_season["number"] = 'absolute'

		for season in elem["seasons"][1:]:
			absolute_season["episodes"].extend(season["episodes"])
		
		del elem["seasons"][1:]

		return elem


	def __extractSerie(self, elem:dict) -> dict:
		"""
		Estrare da elem solo le informazioni importanti che riguardano la serie.

		Args:
		  elem: elemento da cui estrarre le informazioni.

		Returns:
		  Le informazioni estratte.
		"""

		return {
			"title": elem["series"]["title"],
			"path": elem["series"]["path"],
			"tvdbId": elem["series"]["tvdbId"],
			"tvRageId": elem["series"]["tvRageId"],
			"tvMazeId": elem["series"]["tvMazeId"],
			"imdbId": elem["series"]["imdbId"],
			"id": elem["series"]["id"]
		}

	def __extractSeason(self, elem:dict) -> dict:
		"""
		Estrare da elem solo le informazioni importanti che riguardano la stagione.

		Args:
		  elem: elemento da cui estrarre le informazioni.

		Returns:
		  Le informazioni estratte.
		"""

		return {
			"number": elem["seasonNumber"]
		}
	
	def __extractEpisode(self, elem:dict) -> dict:
		"""
		Estrare da elem solo le informazioni importanti che riguardano l'episodio.

		Args:
		  elem: elemento da cui estrarre le informazioni.

		Returns:
		  Le informazioni estratte.
		"""

		return {
			"episodeNumber": elem["episodeNumber"],
			"seasonNumber": elem["seasonNumber"],
			"absoluteEpisodeNumber": elem["absoluteEpisodeNumber"],
			"title": elem["title"],
			"id": elem["id"]
		}