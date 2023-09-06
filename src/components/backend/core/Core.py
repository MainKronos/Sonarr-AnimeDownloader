from . import Constant as ctx
from ..utility import Processor
from ..database import *
from ..connection import *

import logging, logging.handlers
import sys


class Core:

	def __init__(self, *, settings:Settings=None, tags:Tags=None, table:Table=None, sonarr:Sonarr=None, external:ExternalDB=None) -> None:
		"""
		Inizializzazione funzionalità di base.

		Args:
		  settings: Override Settings
		  tags: Override Tags
		  table: Override Table
		  sonarr: Override Sonarr
		  external: Override ExternalDB
		"""

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
		self.processor = Processor(self.sonarr, settings=self.settings, table=self.table, tags=self.tags)

		self.log.debug('Core Inizialized.')

	def __setupLog(self):
		"""Configura la parte riguardante il logger."""

		logger = ctx.LOGGER
		default_formatter = logging.Formatter('%(message)s')

		stream_handler = logging.StreamHandler(sys.stdout)
		stream_handler.terminator = '\n'
		stream_handler.setFormatter(default_formatter)
		logger.addHandler(stream_handler)

		# file_handler = logging.FileHandler(filename='log.log')
		# file_handler.terminator = '\n'
		# file_handler.setFormatter(default_formatter)
		# logger.addHandler(file_handler)

		logger.propagate = True

		self.log = logger

	def run(self):
		"""Avvio del processo di ricerca episodi."""


		self.log.debug('Run `1')