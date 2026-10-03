from . import Constant as ctx
from ..utility import ColoredString as cs
from ..database import *
from ..connection import *
from .Downloader import Downloader
from .Processor import Processor

import logging, logging.handlers
import sys, threading
import time
from typing import Optional
import httpx
import animeworld as aw

class Core(threading.Thread):

	def __init__(self, *, 
		settings:Optional[Settings]=None, 
		tags:Optional[Tags]=None, 
		table:Optional[Table]=None, 
		sonarr:Optional[Sonarr]=None,
		github:Optional[GitHub]=None,
		connections_db:Optional[ConnectionsDB]=None,
		external:Optional[ExternalDB]=None
	):
		"""
		Inizializzazione funzionalità di base.

		Args:
		  settings: Override Settings
		  tags: Override Tags
		  table: Override Table
		  sonarr: Override Sonarr
		  github: Override GitHub
		  connections_db: Override ConnectionsDB
		  external: Override ExternalDB
		"""

		### Setup Thread ###
		super().__init__(name=self.__class__.__name__, daemon=True)

		self.semaphore = threading.Condition()
		self.version = ctx.VERSION

		### Setup logger ###
		self.__setupLog()

		### Setup database ###
		self.settings = settings if settings else Settings(ctx.DATABASE_FOLDER.joinpath('settings.json'))
		self.tags = tags if tags else Tags(ctx.DATABASE_FOLDER.joinpath('tags.json'))
		self.table = table if table else Table(ctx.DATABASE_FOLDER.joinpath('table.json'))
		self.connections_db = connections_db if connections_db else ConnectionsDB(ctx.DATABASE_FOLDER.joinpath('connections.json'), ctx.SCRIPT_FOLDER)
		self.external = external if external else ExternalDB()

		### Fix log level ###
		self.log.setLevel(self.settings["LogLevel"])

		### Setup Connection ###
		self.sonarr = sonarr if sonarr else Sonarr(ctx.SONARR_URL, ctx.API_KEY)
		self.github = github if github else GitHub()
		self.connections = ConnectionsManager(self.connections_db)

		### Setup Logic ###
		aw.SES.base_url = ctx.ANIMEWORLD_URL
		self.processor = Processor(sonarr=self.sonarr, settings=self.settings, table=self.table, tags=self.tags, external=self.external)
		self.downloader = Downloader(settings=self.settings, sonarr=self.sonarr, connections=self.connections, folder=ctx.DOWNLOAD_FOLDER)

		self.error = None

		### Welcome Message ###
		self.log.info(cs.blue(f"┌───────────────────────────────────[{time.strftime('%d %b %Y %H:%M:%S')}]───────────────────────────────────┐"))
		self.log.info(cs.blue(r"│                 _                _____                      _                 _            │"))
		self.log.info(cs.blue(r"│     /\         (_)              |  __ \                    | |               | |           │"))
		self.log.info(cs.blue(r"│    /  \   _ __  _ _ __ ___   ___| |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __  │"))
		self.log.info(cs.blue(r"│   / /\ \ | '_ \| | '_ ` _ \ / _ \ |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__| │"))
		self.log.info(cs.blue(r"│  / ____ \| | | | | | | | | |  __/ |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |    │"))
		self.log.info(cs.blue(r"│ /_/    \_\_| |_|_|_| |_| |_|\___|_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|    │"))
		self.log.info(cs.blue(r"│                                                                                            │"))
		self.log.info(cs.blue(f"└────────────────────────────────────{ctx.VERSION:─^20}────────────────────────────────────┘"))
		self.log.info("")
		self.log.info("Globals")
		self.log.info(f"  ├── {ctx.SONARR_URL = :}")
		self.log.info(f"  ├── {ctx.API_KEY = :}")
		self.log.debug(f"  ├── {ctx.ANIMEWORLD_URL = :}")
		self.log.debug(f"  ├── {ctx.DOWNLOAD_FOLDER = :}")
		self.log.debug(f"  ├── {ctx.DATABASE_FOLDER = :}")
		self.log.debug(f"  ├── {ctx.SCRIPT_FOLDER = :}")
		self.log.info(f"  └── {ctx.VERSION = :}")
		self.log.info("")
		self.log.info("Settings")
		for index, setting in reversed(list(enumerate(self.settings))):
			if index > 0:
				self.log.info(f"  ├── {setting} = {self.settings[setting]}")
			else:
				self.log.info(f"  └── {setting} = {self.settings[setting]}")
		self.log.info("")
		self.log.debug("Tags")
		for index, tag in reversed(list(enumerate(self.tags))):
			if index > 0:
				self.log.debug(f"  ├── {tag['id']} - {tag['name']} ({'🟢' if tag['active'] else '🔴'})")
			else:
				self.log.debug(f"  └── {tag['id']} - {tag['name']} ({'🟢' if tag['active'] else '🔴'})")
		self.log.debug("")
		self.log.debug("Connections")
		for index, connection in reversed(list(enumerate(self.connections_db))):
			if index > 0:
				self.log.debug(f"  ├── {connection['name']} - {connection['script']} ({'🟢' if connection['active'] else '🔴'})")
			else:
				self.log.debug(f"  └── {connection['name']} - {connection['script']} ({'🟢' if connection['active'] else '🔴'})")
		self.log.debug("")


	def __setupLog(self):
		"""Configura la parte riguardante il logger."""

		logger = ctx.LOGGER

		stream_handler = logging.StreamHandler(sys.stdout)
		stream_handler.terminator = '\n'
		stream_handler.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
		logger.addHandler(stream_handler)

		file_handler = logging.FileHandler(filename='log.log', encoding='utf-8', mode='w')
		file_handler.terminator = '\n'
		file_handler.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
		logger.addHandler(file_handler)

		logger.propagate = True

		self.log = logger

	def run(self):
		"""Avvio del processo di ricerca episodi."""
		self.log.info("")
		self.log.info("]────────────────────────────────────────────────────────────────────────────────────────────[")
		self.log.info("")

		# Acquire lock
		self.semaphore.acquire()

		try:
			while True:
				start = time.time()
				self.log.info(f"╭───────────────────────────────────「{time.strftime('%d %b %Y %H:%M:%S')}」───────────────────────────────────╮")

				self.job()
				
				next_run = self.settings['ScanDelay']*60 + start
				wait = next_run - time.time()
				self.log.info(f"╰───────────────────────────────────「{time.strftime('%d %b %Y %H:%M:%S', time.localtime(next_run))}」───────────────────────────────────╯")
				self.log.info("")

				# release lock and wait for next execution
				self.semaphore.wait(timeout=wait)
		except Exception as e:
			# Errore interno non recuperabile
			self.log.critical("]─────────────────────────────────────────[CRITICAL]─────────────────────────────────────────[")
			self.log.exception(e)
			self.error = e

	def job(self):
		"""
		Processo principale di ricerca e download.
		"""

		try:
			self.log.info("")

			missing = self.processor.getData()

			self.log.info("")
			self.log.info("──────────────────────────────────────────────────────────────────────────────────────────────")
			self.log.info("")

			self.downloader.download(missing)

			self.log.info("")
			self.log.info("──────────────────────────────────────────────────────────────────────────────────────────────")
			self.log.info("")
		except aw.DeprecatedLibrary as e:
			self.log.error(cs.red(f"🅴🆁🆁🅾🆁: {e}"))
				
	def wakeUp(self) -> bool:
		"""
		Fa partire immediatamente il processo di ricerca e download.
		"""
		try:
			# acquire lock
			self.semaphore.acquire()
			# resume thread
			self.semaphore.notify()
			# release lock
			self.semaphore.release()
		except RuntimeError as e:
			return False
		else:
			return True



	# def join(self) -> None:
	# 	super().join()
	# 	# Se è stata sollevata un eccezione la propaga
	# 	if self.error: raise self.error