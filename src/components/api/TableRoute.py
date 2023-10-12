from ..backend import Core

from fastapi.routing import APIRouter

def TableRoute(core:Core) -> APIRouter:
	route = APIRouter(prefix='/table', tags=['table'])

	@route.get("/")
	def get_table() -> list[dict]:
		"""
		Restituisce la lista di elementi della tabella.
		
		```json
		[
		...
		  {
		    "absolute": false,
		    "seasons": {
		      "1": [
		        "https://www.animeworld.tv/play/bakuten.MfCW1"
		      ]
		    },
		    "title": "Backflip!!"
		  },
		...
		]
		```
		"""
		return core.table.getData()
	

	return route