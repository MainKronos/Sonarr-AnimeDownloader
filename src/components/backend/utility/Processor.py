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