from ...backend import Core

from apiflask import APIBlueprint, abort, fields

def Tags(core:Core) -> APIBlueprint:

	route = APIBlueprint('tags', __name__, url_prefix='/tags', tag='Tags')
	
	@route.after_request
	def cors(res):
		res.headers['Access-Control-Allow-Origin'] = '*'
		res.headers['Access-Control-Allow-Headers'] = '*'
		res.headers['Access-Control-Allow-Methods'] = '*'
		return res

	@route.get('/')
	def get_tags():
		"""Restituisce i tags."""

		return core.tags.getData()
	
	@route.post('/')
	@route.input({'name':fields.String(),'id': fields.Integer(), 'active': fields.Boolean()})
	def add_tag(json_data:dict):
		"""Aggiunge un tag."""
		
		try:
			core.tags.append(json_data['id'], json_data['name'], json_data['active'])
		except ValueError as e:
			abort(400, str(e))

		return {'message': f"Tag '{json_data['name']}' aggiunto."}
	

	@route.get('/<tag>')
	def get_tag(tag:str|int):
		"""Restituisce le informazioni di un tag."""

		try: tag = int(tag)
		except ValueError: pass

		if tag not in core.tags:
			abort(400, f"Il tag '{tag}' non esiste.")

		return core.tags[tag]

	@route.delete('/<tag>')
	def del_tag(tag:str|int):
		"""Rimuove un tag."""

		if tag not in core.tags:
			abort(400, f"Il tag '{tag}' non esiste.")
		
		tagname = core.tags[tag]["name"]
		
		del core.tags[tag]

		return {'message': f"Tag '{tagname}' eliminato."}
	
	@route.patch('/<tag>/enable')
	def enable_tag(tag:str|int):
		"""Attiva un tag."""

		if tag not in core.tags:
			abort(400, f"Il tag '{tag}' non esiste.")
		
		tagname = core.tags[tag]["name"]
		
		core.tags.enable(tag)
		
		return {'message': f"Tag '{tagname}' attivato."}

	@route.patch('/<tag>/disable')
	def disable_tag(tag:str|int):
		"""Disattiva un tag."""

		if tag not in core.tags:
			abort(400, f"Il tag '{tag}' non esiste.")
		
		tagname = core.tags[tag]["name"]
		
		core.tags.disable(tag)

		return {'message': f"Tag '{tagname}' disattivato."}
	
	@route.patch('/<tag>/toggle')
	def toggle_tag(tag:str|int):
		"""Attiva/Disattiva un tag."""

		if tag not in core.tags:
			abort(400, f"Il tag '{tag}' non esiste.")
		
		tagname = core.tags[tag]["name"]
		
		if core.tags.isActive(tag):
			core.tags.disable(tag)
			return {'message': f"Tag '{tagname}' disattivato."}
		else:
			core.tags.enable(tag)
			return {'message': f"Tag '{tagname}' attivato."}

	return route