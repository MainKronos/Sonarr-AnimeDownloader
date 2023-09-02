from ..core import Constant as ctx
from ..connection import Sonarr
from ..database import *

import logging

class Processor:
	"""Processa i dati che provengono da Sonarr"""

	def __init__(self, sonarr:Sonarr, *, settings:Settings=None, tags:Tags=None, table:Table=None) -> None:
		self.sonarr = sonarr
		self.settings = settings
		self.tags = tags
		self.table = table
		self.log = logging.getLogger(ctx.LOGGER)
	
	def getData(self) -> list:
		"""Restituisce i dati elaborati."""

		return self.__getAllMissing()

	def __getAllMissing(self) -> list:
		"""Ottiene tutta la lista di episodi."""

		missing = []

		for page in range(1,50):
			res = self.sonarr.wantedMissing(page=page)
			res.raise_for_status()
			res = res.json()

			if len(res["records"]) == 0: break

			missing.extend(filter(self.__filter, res['records']))

		return missing


	def __filter(self, elem:dict) -> bool:
		"""Filtra gli episodi."""

		# Controllo che sia effettivamente un anime
		if elem["series"]["seriesType"] != 'anime': return False

		# Controllo i tag
		tag_active = any([self.tags[x] for x in elem["series"]["tags"] if x in self.tags])
		if tag_active and self.settings["TagsMode"] == "BLACKLIST" or not tag_active and self.settings["TagsMode"] == "WHITELIST": return False

		return True
