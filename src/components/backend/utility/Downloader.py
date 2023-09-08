from ..database import Settings
from ..connection import ConnectionsManager, Sonarr
from ..core.Constant import LOGGER
from ..utility import ColoredString as cs

import httpx, re, pathlib
import animeworld as aw
from copy import deepcopy
from functools import reduce
from typing import Callable, Any

class Downloader:
	"""Gestisce il corretto download degli episodi."""

	def __init__(self, settings:Settings, sonarr:Sonarr, connections:ConnectionsManager, folder:pathlib.Path):
		"""
		Args:
		  settings: Impostazioni
		  sonarr: collegamento con Sonarr
		  connections: collegamento con le Connections
		  folder: la cartella di download
		"""

		self.settings = settings
		self.sonarr = sonarr
		self.connections = connections
		self.folder = folder
		self.log = LOGGER
		self.hook = lambda x:None

	def connectHook(self, hook:Callable[[dict[str,Any]], None]):
		"""
		Collega la funzione di hook che verrà richiamata svariate volte durante il download per monitorarne il progresso.

		Args:
		  hook: funzione da richiamare durante il download
		"""
		self.hook = hook

	def download(self, serie:dict):
		"""
		Scarica ogni episodio contenuto nella serie.

		Args:
		  serie: dizionario con le informazioni
		"""

		for season in serie["seasons"]:
			try:
				self.log.info(f"🔎 Ricerca serie '{serie['title']}' stagione {season['number']}.")

				tmp = [aw.Anime(link=x) for x in season["urls"]]

				episodes_str = ", ".join([str(x["episodeNumber"]) for x in season["episodes"]])
				self.log.info(f"🔎 Ricerca episodio {episodes_str}.")
				self.log.info("")

				episodi = reduce(self.flattenEpisodes,[x.getEpisodes() for x in tmp], [])

				for episode in season["episodes"]:
					self.log.info(f"⚙️ Verifica se l'episodio S{episode['seasonNumber']}E{episode['episodeNumber']} è disponibile.")

					# Controllo se è in download su Sonarr
					if self.__isInQueue(episode['id']):
						self.log.info("🔒 L'episodio è già in download su Sonarr.")
						continue

					episodio = None

					if season["number"] == 'absolute':
						# La serie è in formato assoluto
						res = filter(lambda x: x.number == str(episode['absoluteEpisodeNumber']), episodi)
						episodio = next(res, None)
					else:
						# La serie è normale
						res = filter(lambda x: x.number == str(episode['episodeNumber']), episodi)
						episodio = next(res, None)
					
					if not episodio:
						self.log.info("✖️ L'episodio NON è ancora uscito.")
						continue
					
					self.log.info("✔️ L'episodio è disponibile.")
					self.log.warning(f"⏳ Download episodio S{episode['seasonNumber']}E{episode['episodeNumber']}.")

					title = f'{serie["title"]} - S{episode["seasonNumber"]}E{episode["episodeNumber"]}'
					file = episodio.download(title, self.folder, hook=self.hook)

					if not file:
						self.log.warning(f"⚠️ Errore in fase di download.")
						continue
					
					self.log.info("✔️ Dowload Completato.")




			except aw.AnimeNotAvailable as e:
				self.log.info(f'⚠️ {e}')
			except (aw.ServerNotSupported, aw.Error404) as e:
				self.log.warning(cs.yellow(f"🆆🅰🆁🅽🅸🅽🅶: {e}"))
			except (aw.DeprecatedLibrary, httpx.HTTPError) as e:
				self.log.error(cs.red(f"🅴🆁🆁🅾🆁: {e}"))

	def flattenEpisodes(self, base:list[aw.Episodio], elem:list[aw.Episodio]) -> list[aw.Episodio]:
		"""
		Linearizza la lista di episodi che appartengono a più pagine Animeworld e corregge eventuali problemi.

		Args:
			base: lista contenente il risultato della riduzione
			elem: lista di episodi da aggiungere alla base
		"""

		# numero da aggiungere per rendere consecutivi gli episodi di varie stagioni
		limit = 0 if len(base) == 0 else base[-1].number

		for ep in elem:
			if re.search(r'^\d+$', ep.number) is not None: 
				# Se è un episodio intero
				ep.number = str(int(ep.number) + limit)
				base.append(ep)

			elif re.search(r'^\d+\.\d+$', ep.number) is not None: 
				# Se è un episodio fratto
				# lo salta perchè sicuramente uno speciale
				continue 

			elif re.search(r'^\d+-\d+$', ep.number) is not None:
				# Se è un pisodio doppio
				# Duplica l'episodio
				ep_cpy = deepcopy(ep)   

				ep.number = str(int(ep.number.split('-')[0]) + limit)
				ep_cpy.number = str(int(ep.number.split('-')[1]) + limit)

				base.extend([ep,ep_cpy])

		return base
	
	def __isInQueue(self, episodeId:int) -> bool:
		"""
		Controllo se un episodio è in download su Sonarr.

		Args:
		  episode: L'episodio.

		Returns:
		  True se è in download su Sonarr, altrimenti False.
		"""

		# Controllo che non sia già in download su sonarr
		res = self.sonarr.queue()
		res.raise_for_status()
		records = res.json()["records"]

		for record in records:
			if episodeId == record["episodeId"]: return True
		return False
	
	def __moveFile(self, src:pathlib.Path, dest:pathlib.Path):
		pass