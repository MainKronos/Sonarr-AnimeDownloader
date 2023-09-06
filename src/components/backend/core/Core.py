from . import Constant as ctx
from ..utility import Processor
from ..database import *
from ..connection import *

import logging, logging.handlers
import sys, threading
import time

class Core(threading.Thread):

	def __init__(self, *, 
		settings:Settings=None, 
		tags:Tags=None, 
		table:Table=None, 
		sonarr:Sonarr=None,
		github:GitHub=None,
		external:ExternalDB=None
	):
		"""
		Inizializzazione funzionalità di base.

		Args:
		  settings: Override Settings
		  tags: Override Tags
		  table: Override Table
		  sonarr: Override Sonarr
		  github: Override GitHub
		  external: Override ExternalDB
		"""

		### Setup Thread ###
		super().__init__(name=self.__class__.__name__, daemon=True)

		### Setup logger ###
		self.__setupLog()

		### Setup database
		self.settings = settings if settings else Settings(ctx.DATABASE_FOLDER.joinpath('settings.json'))
		self.tags = tags if tags else Tags(ctx.DATABASE_FOLDER.joinpath('tags.json'))
		self.table = table if table else Tags(ctx.DATABASE_FOLDER.joinpath('tags.json'))
		self.external = external if external else ExternalDB()

		### Fix log level
		self.log.setLevel(self.settings["LogLevel"])

		### Setup Connection ###
		self.sonarr = sonarr if sonarr else Sonarr(ctx.SONARR_URL, ctx.API_KEY)
		self.github = github if github else GitHub()
		self.processor = Processor(self.sonarr, settings=self.settings, table=self.table, tags=self.tags)

		self.error = None
		self.log.debug('Core Inizialized.')

	def __setupLog(self):
		"""Configura la parte riguardante il logger."""

		logger = ctx.LOGGER

		stream_handler = logging.StreamHandler(sys.stdout)
		stream_handler.terminator = '\n'
		stream_handler.setFormatter(logging.Formatter('%(levelname)-8s: %(message)s'))
		logger.addHandler(stream_handler)

		# file_handler = logging.FileHandler(filename='log.log')
		# file_handler.terminator = '\n'
		# file_handler.setFormatter(default_formatter)
		# logger.addHandler(file_handler)

		logger.propagate = True

		self.log = logger

	def run(self):
		"""Avvio del processo di ricerca episodi."""
		try:
			while True:
				start = time.time()
				self.job()
				next_run = self.settings['ScanDelay']*60 + start
				wait = next_run - time.time()
				if wait > 0: time.sleep(wait)
		except Exception as e:
			# Errore interno non recuperabile
			self.error = e
	
	def job(self):
		"""
		Processo principale di ricerca e download.
		"""
		missing = self.processor.getData()

		

	def join(self) -> None:
		super().join()
		# Se è stata sollevata un eccezione la propaga
		if self.error: raise self.error