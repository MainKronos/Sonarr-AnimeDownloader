import unittest

from src.components.backend.core.Core import ctx, Core

import pathlib
import sys

class TestGeneral(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		ctx.SONARR_URL = "http://netvault:8989/"
		ctx.API_KEY = "f10994e9f3494368a31a3088aba6b9fc"
		ctx.DOWNLOAD_FOLDER = pathlib.Path('./tests').absolute()
		ctx.DATABASE_FOLDER = pathlib.Path("./tests/database").absolute()
		ctx.SCRIPT_FOLDER = pathlib.Path("./tests/script").absolute()


	def test(self):
		core = Core()

		core.run()

if __name__ == '__main__':
	unittest.main(verbosity=2, buffer=True)