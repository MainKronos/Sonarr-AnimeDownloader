import os
import pathlib
import sys

from components.backend.core.Core import Core, ctx
from components.api import API

import pathlib
import sys, json
import uvicorn

ctx.DOWNLOAD_FOLDER = pathlib.Path('./tests/downloads').absolute()
ctx.DATABASE_FOLDER = pathlib.Path("./tests/database").absolute()
ctx.SCRIPT_FOLDER = pathlib.Path("./tests/script").absolute()
ctx.SONARR_URL = "http://netvault:8989/"
ctx.API_KEY = "f10994e9f3494368a31a3088aba6b9fc"
ctx.VERSION = "dev"

def main():

	# Carico il core
	core = Core()
	
	# Cario la pagina web
	app = API(core)

	return app

if __name__ == "__main__":
    uvicorn.run("dev_api:main", port=5000, log_level="info", reload=True, factory=True)