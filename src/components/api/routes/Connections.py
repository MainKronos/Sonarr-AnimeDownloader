from ...backend import Core

from apiflask import APIBlueprint, abort, fields

def Connections(core:Core) -> APIBlueprint:

	route = APIBlueprint('connections', __name__, url_prefix='/connections', tag='Connections')
	
	@route.after_request
	def cors(res):
		res.headers['Access-Control-Allow-Origin'] = '*'
		res.headers['Access-Control-Allow-Headers'] = '*'
		res.headers['Access-Control-Allow-Methods'] = '*'
		return res
	
	@route.get('/')
	def get_connections():
		"""Restituisce le connections."""

		return core.connections_db.getData()
	
	@route.get('/<script>')
	def get_connection(script:str):
		"""Restituisce una connection in base al nome dello script."""

		for connection in core.connections_db:
			if connection["script"] == script:
				return connection
		
		abort(400, f"il file {script} non esiste.")
	
	@route.delete('/<script>')
	def del_connection(script:str):
		"""Rimuove una connection."""

		try:
			core.connections_db.deleteByScript(script)
			return {'message': f"La Connection {script} è stata eliminata."}
		except KeyError:
			abort(400, f"La connection '{script}' non esiste.")
	
	@route.post('/')
	@route.input({'script':fields.String(), 'active': fields.Boolean()})
	def add_connection(json_data:dict):
		"""Aggiunge una connection."""
		
		script = json_data["script"]
		active = json_data["active"]

		try:
			core.connections_db.append(script, script, active)
			return {'message': f"La Connection {script} è stata aggiunta."}
		except ValueError as e:
			abort(400, str(e))
		except FileNotFoundError:
			abort(400, f"il file {script} non esiste.")
	
	@route.patch('/<script>/enable')
	def enable_connection(script:str):
		"""Attiva una connection."""

		try:
			core.connections_db.enableByScript(script)
			return {'message': f"La Connection {script} è stata attivata."}
		except KeyError:
			abort(400, f"La connection '{script}' non esiste.")

	@route.patch('/<script>/disable')
	def disable_connection(script:str):
		"""Disattiva una connection."""

		try:
			core.connections_db.disableByScript(script)
			return {'message': f"La Connection {script} è stata disattivata."}
		except KeyError:
			abort(400, f"La connection '{script}' non esiste.")
	
	@route.patch('/<script>/toggle')
	def toggle_connection(script:str):
		"""Attiva/Disattiva una connection."""

		try:
			val = core.connections_db.toggleByScript(script)
			if(val):
				return {'message': f"La Connection {script} è stata attivata."}
			else:
				return {'message': f"La Connection {script} è stata disattivata."}
		except KeyError:
			abort(400, f"La connection '{script}' non esiste.")
	

	return route