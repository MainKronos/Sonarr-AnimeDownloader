import logging
from logging import _Level

class Logger(logging.Logger):
	def __init__(self, name: str, level: _Level = 0) -> None:
		super().__init__(name, level)