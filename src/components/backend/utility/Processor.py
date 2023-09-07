from ..core import Constant as ctx
from ..connection import Sonarr, ExternalDB
from ..database import *

import logging
from functools import reduce

class Processor:
	"""Processa i dati che provengono da Sonarr"""

	def __init__(self, sonarr:Sonarr, *, settings:Settings, tags:Tags, table:Table, external:ExternalDB):
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

		# Rimuovo le serie e stagioni non valide
		missing = filter(self.__filter, missing)

		# Aggiorno il database esterno
		self.external.sync()

		# Collego gli url per il download e rimuovo le stagioni che non fanno match
		missing = list(filter(self.__bindUrl, missing))

		self.log.info("")
		self.log.info("──────────────────────────────────────────────────────────────────────────────────────────────")
		self.log.info("")

		return missing

	def getAllMissing(self) -> list:
		"""
		Ottiene tutta la lista di episodi formattati.
		
		Returns:
		  La lista di episodi mancanti.
		"""

		missing = []

		for page in range(1,50):
			res = self.sonarr.wantedMissing(page=page)
			res.raise_for_status()
			res = res.json()

			if len(res["records"]) == 0: break

			missing.extend(res['records'])

		# Riduco le informazioni a solo quelle indispensabili
		missing = reduce(self.__reduce, missing, [])

		return missing

	### FUNCTIONS ###

	def __filter(self, elem:dict) -> bool:
		"""
		Filtra le serie e stagioni non valide.

		Args:
		  elem: serie da filtrare.
		
		Returns:
		  True da prendere / False da scartare
		"""

		# Controllo che sia effettivamente un anime
		if elem["type"] != 'anime': 
			self.log.debug(f"❌ Serie '{elem['title']}' scartata perchè non è di tipo anime.")
			return False

		# Controllo i tag
		active_tags = [x['id'] for x in self.tags if self.tags.isActive(x['id'])]
		serie_tags = [x for x in elem["tags"] if x in active_tags]
		if any(serie_tags) and self.settings["TagsMode"] == "BLACKLIST":
			self.log.debug(f"❌ Serie '{elem['title']}' scartata perchè ha uno dei tag [{', '.join([self.tags(x)['name'] for x in serie_tags])}].")
			return False
		if not any(serie_tags) and self.settings["TagsMode"] == "WHITELIST":
			self.log.debug(f"❌ Serie '{elem['title']}' scartata perchè non ha nessuno dei tag [{', '.join([self.tags(x)['name'] for x in active_tags])}].")
			return False

		def filterSeason(season:dict) -> bool:
			"""Filtra le stagioni."""
			# Controllo che non siano episodi speciali
			if season["number"] == 0:
				self.log.debug(f"❌ Stagione {season['number']} della serie '{elem['title']}' scartata perchè contiene episodi speciali.")
				return False
			return True

		# Filtro le stagioni non valide
		elem["seasons"] = list(filter(filterSeason,elem["seasons"]))

		# Controllo che la serie contenga delle stagioni
		if len(elem["seasons"]) == 0: return False

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
	
	def __bindUrl(self, elem:dict) -> bool:
		"""
		Collega l'url di download a tutte le stagioni contenute nella serie in elem, se non trova nulla rimuove la stagione.

		Args:
		  elem: serie che contiene le stagioni a cui verranno aggiunti gli url di download

		Returns:
		  True da prendere / False da scartare
		"""

		table_entry = None
		title = elem["title"]
		if title not in self.table: 
			if not self.settings["AutoBind"]:
				# Se non è attiva la ricerca automatica provo a trovare dei url
				self.log.debug(f"❌ Serie '{title}' scartata perchè non è presente nella TABELLA DI CONVERSIONE.")
				return False
		else:
			table_entry = self.table[title]

			if table_entry["absolute"]:
				# Se la serie è in formato 'absolute'
				elem = self.__convertToAbsolute(elem)


		def filterSeason(season:dict) -> bool:
			"""Filtra le stagioni."""
			season_number = str(season["number"])
			if table_entry and season_number in table_entry["seasons"]:
				# Se la stagione è presente nella tabella
				if len(table_entry["seasons"][season_number]) == 0:
					# Se non sono presenti dei url
					self.log.debug(f"❌ Stagione {season['number']} della serie '{title}' scartata per mancanza di url.")
					return False
				else:
					season["urls"].extend(list(table_entry["seasons"][season_number]))
					return True
			else:
				# Se la stagione NON è presente in tabella
				self.log.debug(f"⚠️ Stagione {season['number']} della serie '{title}' non è presente nella TABELLA DI CONVERSIONE.")
				if not self.settings["AutoBind"]:
					return False
				else:
					# Se è attiva la ricerca automatica provo a trovare dei url
					if season['number'] == 'absolute':
						# Se la stagione è di tipo absolute
						self.debug(f"⛔ La ricerca automatica degli url di download è incompatibile con le serie ad ordinamento assoluto.")
						return False
					else:
						res = self.external.find(title, season["number"], elem["tvdbId"])
						if res is None:
							# Se non ho trovato nulla
							self.log.debug(f"🔴 Ricerca automatica url per la stagione {season['number']} della serie '{elem['title']}': nessun risultato trovato.")
							return False
						else:
							self.log.warning(f"🟢 Ricerca automatica url per la stagione {season['number']} della serie '{elem['title']}': {res['url']}")
							# Altrimenti aggiungo ciò che ho trovato
							season["urls"].append(res["url"])

							# Adesso devo aggiornare la tabella, aggiungendo l'url
							self.table.appendUrl(title, season['number'], res["url"])

							return True

		# Aggiungo gli url alle stagioni
		elem["seasons"] = list(filter(filterSeason, elem["seasons"]))

		# Se ha almeno una stagione la prendo altrimenti la lascio
		return len(elem["seasons"]) > 0
	
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
			"id": elem["series"]["id"],
			"type": elem["series"]["seriesType"],
			"tags": elem["series"]["tags"]
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
			"absoluteEpisodeNumber": elem["absoluteEpisodeNumber"] if "absoluteEpisodeNumber" in elem else None,
			"title": elem["title"],
			"id": elem["id"]
		}