import pathlib

from components.backend.core.Core import Core, ctx
from components.api import API

ctx.DOWNLOAD_FOLDER = pathlib.Path('./tests/downloads').absolute()
ctx.DATABASE_FOLDER = pathlib.Path("./tests/database").absolute()
ctx.SCRIPT_FOLDER = pathlib.Path("./tests/script").absolute()
ctx.SONARR_URL = "http://netvault:8989"
ctx.API_KEY = "f10994e9f3494368a31a3088aba6b9fc"
ctx.VERSION = "dev"

def main():

	# Carico il core
	core = Core()
	
	# Cario la pagina web
	app = API(core)

	return app

if __name__ == "__main__":
    main().run(debug=True, host='0.0.0.0', use_reloader=True)