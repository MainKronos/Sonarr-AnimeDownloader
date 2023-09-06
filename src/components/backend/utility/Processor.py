from ..core import Constant as ctx
from ..connection import Sonarr, ExternalDB
from ..database import *

import logging
from functools import reduce

class Processor:
	"""Processa i dati che provengono da Sonarr"""

	def __init__(self, sonarr:Sonarr, *, settings:Settings, tags:Tags, table:Table, external:ExternalDB) -> None:
		self.sonarr = sonarr
		self.settings = settings
		self.tags = tags
		self.table = table
		self.external = external
		self.log = ctx.LOGGER
	
	def getData(self) -> list:
		"""Restituisce i dati elaborati."""

		# Raccolgo tutti gli episodi
		missing = self.getAllMissing()

		# Riduco le informazioni a solo quelle indispensabili
		missing = reduce(self.__reduce, missing, [])

		# Aggiorno il database esterno
		self.external.sync()

		# Collego gli url per il download
		missing = filter(self.__bindUrl, missing)

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

	### FUNCTIONS ###

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
			season["urls"] = []
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
		if title not in self.table: return elem

		table_entry = self.table[title]

		if table_entry["absolute"]:
			# Se la serie è in formato 'absolute'
			elem = self.__convertToAbsolute(elem)
			elem["seasons"][0]["urls"].extend(list(table_entry["seasons"]["absolute"]))
			return elem
		else:
			for season in elem["seasons"]:
				season_number = str(season["number"])
				if season_number in table_entry["seasons"]:
					# Se la stagione è presente nella tabella
					season["urls"].extend(list(table_entry["seasons"][season_number]))
				else:
					# Se la stagione NON è presente in tabella
					if self.settings["AutoBind"]:
						# Se è attiva la ricerca automatica provo a trovare dei url
						res = self.external.find(elem["title"], season["number"], elem["tvdbId"])
						# Se non ho trovato nulla continuo
						if res is None: continue
						# Altrimenti aggiungo ciò che ho trovato
						season["urls"].append(res["url"])

			return elem
	
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

	### EXTRACTOR ###

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