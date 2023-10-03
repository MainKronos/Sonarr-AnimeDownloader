import httpx
import animeworld as aw
from typing import Optional

from ..core.Constant import LOGGER

class ExternalDB:
	"""
	Collegamento con le informazioni che si trovano su GitHub.
	https://github.com/Fribb/anime-lists
	"""

	def __init__(self):
		self.log = LOGGER
		self.client = httpx.Client()
		self._data = []
	
	def sync(self) -> list:
		"""
		Sincronizza i dati interni con il database esterno.

		Returns:
		  Tutti i dati aggiornati.
		"""

		res = self.client.get("https://raw.githubusercontent.com/Fribb/anime-lists/master/anime-list-full.json")
		res.raise_for_status()
		self._data = res.json()
		return self._data
	
	def getData(self)-> list:
		"""
		Restituisce tutti i dati.

		Returns:
		  I dati nel database.
		"""
		return list(self._data)
	
	def find(self, title:str, season:int, tvdb_id:int) -> Optional[dict[str, str]]:
		"""
		Cerca un url per il download.

		Args:
		  title: titolo dell'anime.
		  season: stagione dell'anime.
		  tvdb_id: ID di thetvdb.
		
		Returns:
		  Un dizionario con nome e url trovato.
		"""

		# Ottengo un elenco di ID di MyAnimeList che fanno match
		mal_ids = []
		for info in self._data:
			if "thetvdb_id" not in info: continue
			if "mal_id" not in info: continue
			if "type" not in info: continue
			if info["thetvdb_id"] != tvdb_id: continue
			if info["type"] != "TV": continue

			mal_ids.append(info["mal_id"])
		
		# Se non ho trovato nulla ritorno None
		if len(mal_ids) == 0: return None

		# Ottengo tutti i risultati da animewolrd ricercando solamente con il nome dell'anime
		res = aw.find(title)

		# Filtro i risultati
		res = list(filter(lambda x: x["malId"] in mal_ids, res))

		# Se non ho trovato nulla ritorno None
		if len(res) == 0: return None

		# Converto le stagioni in numeri
		def conv2num(x):
			if x["season"] == 'winter':
				x["season"] = 0
			elif x["season"] == 'spring':
				x["season"] = 1
			elif x["season"] == 'summer':
				x["season"] = 2
			else:
				x["season"] = 3
			return x
		res = list(map(conv2num, res))

		# Riordino per data
		res.sort(key=lambda x: (x["year"], x["season"]), reverse=True)

		# Controllo se esiste la stagione
		if len(res) < season: return None

		return {
			"name": res[season-1]["name"],
			"url": res[season-1]["link"]
		}