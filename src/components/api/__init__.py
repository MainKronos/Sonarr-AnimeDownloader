from ..backend import Core

from typing import Union, TypedDict
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from .TableRoute import TableRoute

def API(core:Core) -> FastAPI:
	api = APIRouter(prefix='/api')
	
	@api.get("/version")
	def get_version() -> TypedDict('',{'version':str}):
		"""
		Restituisce il numero di versione.

		```json
		{'version': 'dev'}
		```
		"""
		return {"version": core.version}
	
	api.include_router(TableRoute(core))
	
	app = FastAPI(
		title='Sonarr-AnimeDownloader',
		summary='API',
		version=core.version
	)
	app.include_router(api)
	app.add_middleware(
		CORSMiddleware,
		allow_origins=['*'],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)
	return app