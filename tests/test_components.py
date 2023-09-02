import unittest

from src.components.backend.core.Core import ctx, Core
from src.components.backend.connection.Sonarr import Sonarr

from mockup import TestSonarr

import pathlib
import sys, json

ctx.DOWNLOAD_FOLDER = pathlib.Path('./tests').absolute()
ctx.DATABASE_FOLDER = pathlib.Path("./tests/database").absolute()
ctx.SCRIPT_FOLDER = pathlib.Path("./tests/script").absolute()
ctx.SONARR_URL = "http://netvault:8989/"
ctx.API_KEY = "f10994e9f3494368a31a3088aba6b9fc"

DUMP_FOLDER = pathlib.Path('./tests/dump').absolute()		

class TestGeneral(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""Inizializza il nucleo."""
		cls.core = Core()

	def testSonarr(self):
		with open(DUMP_FOLDER.joinpath('wanted_missing.json'), 'w') as f:
			json.dump(self.core.sonarr.wantedMissing(50).json(), f)

		with open(DUMP_FOLDER.joinpath('tags.json'), 'w') as f:
			json.dump(self.core.sonarr.tags().json(), f)
		
		with open(DUMP_FOLDER.joinpath('queue.json'), 'w') as f:
			json.dump(self.core.sonarr.queue().json(), f)
		
		with open(DUMP_FOLDER.joinpath('episode.json'), 'w') as f:
			json.dump(self.core.sonarr.episode(16639).json(), f)
		
		with open(DUMP_FOLDER.joinpath('serie.json'), 'w') as f:
			json.dump(self.core.sonarr.serie(340).json(), f)
		
		with open(DUMP_FOLDER.joinpath('system_status.json'), 'w') as f:
			json.dump(self.core.sonarr.systemStatus().json(), f)

if __name__ == '__main__':
	unittest.main(verbosity=2, buffer=True)