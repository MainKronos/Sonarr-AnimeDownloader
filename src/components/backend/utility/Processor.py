from ..core import Core

class Processor:
	"""Processa i dati che provengono da Sonarr"""

	def __init__(self, core:Core) -> None:
		self.core = core