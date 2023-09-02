from . import Constant as ctx
from ..utility import Processor
from ..database import *
from ..connection import *

import logging, logging.handlers
import sys


class Core:

	def __init__(self, *, settings:Settings=None, tags:Tags=None, table:Table=None, sonarr:Sonarr=None) -> None:
		"""
		Inizializzazione funzionalità di base.

		Args:
		  settings: Override settings
		  tags: Override tags
		  table: Override table
		  sonarr: Override sonarr
		"""

		### Setup database
		self.settings = settings if settings else Settings(ctx.DATABASE_FOLDER.joinpath('settings.json'))
		self.tags = tags if tags else Tags(ctx.DATABASE_FOLDER.joinpath('tags.json'))
		self.table = table if table else Tags(ctx.DATABASE_FOLDER.joinpath('tags.json'))

		### Setup logger ###
		self.__setupLog()
		self.log.setLevel(self.settings["LogLevel"])

		### Setup Connection ###
		self.sonarr = sonarr if sonarr else Sonarr(ctx.SONARR_URL, ctx.API_KEY)
		self.processor = Processor(self.sonarr, settings=self.settings, table=self.table, tags=self.tags)

		self.log.debug('Core Inizialized.')

	def __setupLog(self):
		"""Configura la parte riguardante il logger."""

		default_formatter = logging.Formatter('%(message)s')

		stream_handler = logging.StreamHandler(sys.stdout)
		stream_handler.terminator = '\n'
		stream_handler.setFormatter(default_formatter)

		file_handler = logging.FileHandler(filename='log.log')
		file_handler.terminator = '\n'
		file_handler.setFormatter(default_formatter)

		logger = logging.getLogger(ctx.LOGGER)
		logger.addHandler(stream_handler)
		logger.addHandler(file_handler)
		logger.propagate = True

		self.log = logger

	def run(self):
		"""Avvio del processo di ricerca episodi."""


		self.log.debug('Run `1')