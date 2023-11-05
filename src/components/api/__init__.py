from ..backend import Core

from typing import Union, TypedDict
from apiflask import APIFlask, APIBlueprint

from .routes.Table import Table
from .routes.Settings import Settings
from .routes.Tags import Tags

import time

def API(core:Core) -> APIFlask:
	app = APIFlask(
		__name__,
		title='Sonarr-AnimeDownloader',
		version=core.version
	)

	app.config['AUTO_404_RESPONSE'] = False
	app.config['AUTO_VALIDATION_ERROR_RESPONSE'] = False

	@app.after_request
	def cors(res):
		res.headers['Access-Control-Allow-Origin'] = '*'
		return res

	api = APIBlueprint('api', __name__, url_prefix='/api', tag='General')
	
	@api.get("/version")
	def get_version():
		"""
		Restituisce il numero di versione.
		"""
		# time.sleep(5)
		return {"version": core.version}
	
	api.register_blueprint(Table(core))
	api.register_blueprint(Settings(core))
	api.register_blueprint(Tags(core))
	app.register_blueprint(api)
	return app