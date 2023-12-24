from ...backend import Core

from apiflask import APIBlueprint, abort, fields

def Table(core:Core) -> APIBlueprint:
	route = APIBlueprint('table', __name__, url_prefix='/table', tag='Table')
	
	@route.after_request
	def cors(res):
		res.headers['Access-Control-Allow-Origin'] = '*'
		res.headers['Access-Control-Allow-Headers'] = '*'
		res.headers['Access-Control-Allow-Methods'] = '*'
		return res

	@route.get("/")
	def get_table() -> list[dict]:
		"""Restituisce la lista di elementi della tabella."""
		return core.table.getData()
	
	@route.get('/<title>')
	def get_serie(title:str):
		"""Restituisce le informazioni di una serie."""
		if not title in core.table:
			abort(400, f"La serie '{title}' non esiste.")
	
		return core.table[title]	
	
	@route.get('/<title>/<season>')
	def get_links(title:str, season:int):
		"""Restituisce tutti i link di una stagione."""

		season = str(season)
		serie = get_serie(title)
		if not season in serie["seasons"]:
			abort(400, f"La stagione '{season}' non esiste.")
		
		return serie["seasons"][season]	

	@route.delete('/<title>')
	def del_serie(title:str):
		"""Rimuove una serie."""
		if not title in core.table:
			abort(400, f"La serie '{title}' non esiste.")
	
		core.table.removeSerie(title)

		return {"message": f"Serie '{title}' rimossa."}
	
	@route.delete('/<title>/<season>')
	def del_season(title:str, season:int):
		"""Rimuove una stagione."""

		serie = get_serie(title)
		if not season in serie["seasons"]:
			abort(400, f"La stagione '{season}' non esiste.")
		
		core.table.removeSeason(title, season)

		return {"message": f"Stagione '{season}' rimossa."}
	
	@route.delete('/<title>/<season>/<path:link>')
	def del_link(title:str, season:int, link:str):
		"""Rimuove un link."""

		links = get_links(title, season)
		if not link in links:
			abort(400, f"Il link '{link}' non esiste.")
		
		core.table.removeUrl(title, season, link)

		return {"message": f"Link '{link}' rimosso."}


	@route.post('/')
	@route.input({'title':fields.String(),'absolute': fields.Boolean()})
	def add_serie(json_data:dict):
		"""Aggiunge una nuova serie."""

		title:str = json_data['title']
		absolute:bool = json_data['absolute']

		if not core.table.appendSerie(title, absolute):
			abort(409, f"La serie '{title}' è già presente.")
		
		return {"message": f"Serie '{title}' aggiunta."}

	@route.post('/<title>')
	@route.input({'season':fields.Integer()})
	def add_season(title:str, json_data:dict):
		"""Aggiunge una nuova stagione."""

		season:int = json_data['season']

		if not core.table.appendSeason(title, season):
			abort(409, f"Conflitto stagione '{season}'.")
		
		return {"message": f"Stagione '{season}' aggiunta."}
	
	@route.post('/<title>/<season>')
	@route.input({'links':fields.List(fields.String())})
	def add_links(title:str, season:int, json_data:dict):
		"""Aggiunge dei links a una stagione."""

		links:list[str] = json_data['links']

		if not core.table.appendUrls(title, season, links):
			abort(409, f"Conflitto links {links}.")
		
		return {"message": f"Links {links} aggiunti."}
	
	@route.patch('/<title>')
	@route.input({'title':fields.String()})
	def edit_serie(title:str, json_data:dict):
		"""Rinomina il titolo di una serie."""

		new_title:str = json_data['title']

		if not title in core.table:
			abort(400, f"La serie '{title}' non esiste.")
	
		if not core.table.renameSerie(title, new_title):
			abort(409, f"Il titolo '{new_title}' esiste già.")

		return {"message": f"Serie '{new_title}' aggiornata."}
	
	@route.patch('/<title>/<season>')
	@route.input({'season':fields.Integer()})
	def edit_season(title:str, season:int, json_data:dict):
		"""Rinomina una stagione."""

		season = str(season)
		new_season:str = str(json_data['season'])
		serie = get_serie(title)
		if not season in serie["seasons"]:
			abort(400, f"La stagione '{season}' non esiste.")
		
		if not core.table.renameSeason(title, season, new_season):
			abort(409, f"La stagione '{new_season}' esiste già.")

		return {"message": f"Stagione '{new_season}' aggiornata."}
	
	@route.patch('/<title>/<season>/<path:link>')
	@route.input({'link':fields.String()})
	def edit_link(title:str, season:int, link:str, json_data:dict):
		"""Rinomina un link."""

		new_link:str = json_data['link']
		links = get_links(title, season)
		if not link in links:
			abort(400, f"Il link '{link}' non esiste.")
		
		if not core.table.renameUrl(title, season, link, new_link):
			abort(409, f"Il link '{new_link}' esiste già.")

		return {"message": f"Link '{new_link}' aggiornato."}


	return route