from . import Constant as ctx
from ..utility import Processor
from ..database import *
from ..connection import *

import logging, logging.handlers
import sys


class Core:

	def __init__(self) -> None:

		### SETUP ###
		self.__setupDatabase()
		self.__setupConnection()
		self.__setupLog()

		self.log.debug('Core Inizialized.')

	def __setupDatabase(self):
		"""Configura le classi che gestiscono i database."""
		self.settings = Settings(ctx.DATABASE_FOLDER.joinpath('settings.json'))
		self.tags = Tags(ctx.DATABASE_FOLDER.joinpath('tags.json'))
		self.table = Tags(ctx.DATABASE_FOLDER.joinpath('tags.json'))
	
	def __setupConnection(self):
		"""Configura la parte di collegamento verso l'esterno."""

		self.sonarr = Sonarr(ctx.SONARR_URL, ctx.API_KEY)
		self.processor = Processor(self)

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
		logger.setLevel(self.settings["LogLevel"])
		logger.propagate = True

		self.log = logger

	def run(self):
		self.log.debug('Run `1')