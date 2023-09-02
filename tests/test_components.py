import unittest

from src.components.backend.core.Core import ctx, Core

import pathlib

ctx.SONARR_URL = "http://netvault:8989/"
ctx.API_KEY = "f10994e9f3494368a31a3088aba6b9fc"
ctx.DOWNLOAD_FOLDER = pathlib.Path('./tests').absolute()
ctx.DATABASE_FOLDER = pathlib.Path("./tests/database").absolute()
ctx.SCRIPT_FOLDER = pathlib.Path("./tests/script").absolute()

class TestGeneral(unittest.TestCase):
	def test(self):
		core = Core()

if __name__ == '__main__':
	unittest.main(verbosity=2)