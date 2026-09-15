from ..database import Settings
from ..connection import ConnectionsManager, Sonarr
from .Constant import LOGGER
from ..utility import ColoredString as cs

import httpx, re, pathlib, time
import shutil, tenacity
import animeworld as aw
from copy import deepcopy
from functools import reduce
from typing import Callable, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed


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

	def download(self, series:List[dict]):
		"""
		Scarica gli episodi mancanti di tutte le serie fornite.
		Il numero massimo di download eseguiti in parallelo è definito dall'impostazione 'MaxConcurrentDownloads'.

		Args:
		  series: lista di dizionari con le informazioni delle serie
		"""

		max_workers = max(1, int(self.settings["MaxConcurrentDownloads"]))
		queued_ids = self.__getQueuedEpisodeIds()

		with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="Downloader") as executor:
			futures = []

			for serie in series:
				for season in serie["seasons"]:
					try:
						self.log.info(f"🔎 Ricerca serie '{serie['title']}' stagione {season['number']}.")

						tmp = [aw.Anime(link=x) for x in season["urls"]]

						episodes_str = ", ".join([str(x["episodeNumber"]) for x in season["episodes"]])
						self.log.info(f"🔎 Ricerca episodio {episodes_str}.")

						episodi:List[aw.Episodio] = reduce(self.flattenEpisodes,[x.getEpisodes() for x in tmp], [])

						for episode in season["episodes"]:
							self.log.info("")
							self.log.info(f"⚙️ Verifica se l'episodio S{episode['seasonNumber']}E{episode['episodeNumber']} di '{serie['title']}' è disponibile.")

							# Controllo se è in download su Sonarr
							if episode['id'] in queued_ids:
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

							self.log.info("✔️ L'episodio è disponibile, messo in coda per il download.")

							futures.append(executor.submit(self.__downloadEpisode, serie, episode, episodio))

					except aw.AnimeNotAvailable as e:
						self.log.info(f'⚠️ {e}')
					except (aw.ServerNotSupported, aw.Error404) as e:
						self.log.warning(cs.yellow(f"🆆🅰🆁🅽🅸🅽🅶: {e}"))

			for future in as_completed(futures):
				try:
					future.result()
				except aw.AnimeNotAvailable as e:
					self.log.info(f'⚠️ {e}')
				except (aw.ServerNotSupported, aw.Error404) as e:
					self.log.warning(cs.yellow(f"🆆🅰🆁🅽🅸🅽🅶: {e}"))
				except Exception as e:
					self.log.error(f"✖️ Errore imprevisto durante il download: {e}")

	def __downloadEpisode(self, serie:dict, episode:dict, episodio:'aw.Episodio') -> None:
		"""
		Scarica un singolo episodio e ne gestisce lo spostamento, la rinomina e la notifica.
		Pensato per essere eseguito in un thread del pool di download.

		Args:
		  serie: la serie a cui appartiene l'episodio
		  episode: l'episodio da scaricare
		  episodio: l'oggetto animeworld da cui scaricare l'episodio
		"""

		title = f'{serie["title"]} - S{episode["seasonNumber"]}E{episode["episodeNumber"]}'

		self.log.warning(f"⏳ Download episodio {title}.")
		file = episodio.download(title, self.folder, hook=self.hook)

		if not file:
			self.log.warning(f"⚠️ Errore in fase di download di {title}.")
			return

		file = self.folder.joinpath(file)

		self.log.info(f"✔️ Download completato: {title}.")

		if self.settings["MoveEp"]:
			# Se l'episodio deve essere spostato

			destination = pathlib.Path(serie["path"])
			self.log.warning(f"⏳ Spostamento episodio {title} in {destination}.")
			if not self.__moveFile(file, destination):
				self.log.error(f"✖️ Fallito spostamento episodio {title}.")
				return

			self.log.info(f"✔️ Episodio {title} spostato.")
			# Dopo aver spostato il file faccio scansionare a Sonarr la serie per trovarlo
			self.log.info(f"⏳ Aggiornamento serie '{serie['title']}'.")
			self.sonarr.commandRescanSeries(serie['id'])

			if self.settings["RenameEp"]:
				# Se l'episodio deve essere rinominato
				self.log.info(f"⏳ Rinominando l'episodio {title}.")

				# Aspetto 2s che Sonarr abbia finito di ricaricare la serie
				time.sleep(2)

				# Chiedo a Sonarr di rinominare l'episodio scaricato
				self.__renameFile(episode['id'], serie['id'])

				self.log.info(f"✔️ Episodio {title} rinominato.")

		# Invio una notifica tramite Connections
		self.log.info(f'✉️ Inviando il messaggio tramite Connections per {title}.')
		self.connections.send(f"*Episode Downloaded*\n{serie['title']} - {episode['seasonNumber']}x{episode['episodeNumber']} - {episode['title']}")

	def flattenEpisodes(self, base:list[aw.Episodio], elem:list[aw.Episodio]) -> list[aw.Episodio]:
		"""
		Linearizza la lista di episodi che appartengono a più pagine Animeworld e corregge eventuali problemi.

		Args:
			base: lista contenente il risultato della riduzione
			elem: lista di episodi da aggiungere alla base
		"""

		# numero da aggiungere per rendere consecutivi gli episodi di varie stagioni
		limit = 0 if len(base) == 0 else int(base[-1].number)

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
	
	def __getQueuedEpisodeIds(self) -> set:
		"""
		Ottiene gli id di tutti gli episodi già in download su Sonarr.

		Returns:
		  L'insieme degli id degli episodi in coda su Sonarr.
		"""

		res = self.sonarr.queue()
		res.raise_for_status()
		records = res.json()["records"]

		return {record["episodeId"] for record in records}
	
	def __moveFile(self, src:pathlib.Path, dst:pathlib.Path) -> pathlib.Path:
		"""
		Sposta il file da src a dst.

		Args:
		  src: file da spostare
		  dst: cartella di destinazione
		
		Returns:
		  La path che punta al file spostato.
		"""

		if not src.is_file():
			raise FileNotFoundError(src)

		# Controllo se la cartella di destinazione non sia una cartella windows
		if re.match(r"\w:", str(dst)):
			dst = pathlib.PureWindowsPath(dst).as_posix()
			dst = pathlib.PosixPath(re.sub(r"\w:","",dst))
		
		if not dst.is_dir():
			# Se la cartella non esiste viene creata
			# (exist_ok=True evita errori se un altro download parallelo l'ha già creata)
			dst.mkdir(parents=True, exist_ok=True)
			self.log.warning(f'⚠️ La cartella {dst} è stata creata.')

		dst = dst.joinpath(src.name)
		return shutil.move(src,dst)
	
	@tenacity.retry(reraise=True, stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(2))
	def __renameFile(self, episode_id:int, serie_id:int) -> None:
		"""
		Rinomina il file seguendo la formattazione definita su Sonarr.

		Args:
		  episode_id: id_episodio su Sonarr
		  serie_id: id della serie su Sonarr
		"""

		res = self.sonarr.episode(episode_id)
		res.raise_for_status()
		res = res.json()

		if "episodeFile" not in res: raise Exception("Episodio Non trovato")

		file_id = res["episodeFile"]["id"]
		self.sonarr.commandRenameFiles(serie_id,[file_id])
