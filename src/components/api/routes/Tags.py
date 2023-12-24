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
		"""Aggiunge un tag."""
		
		try: tag = int(tag)
		except ValueError: pass

		if tag not in core.tags:
			abort(400, f"Il tag '{tag}' non esiste.")
		
		del core.tags[tag]

		return {'message': f"Tag '{tag}' eliminato."}
	
	@route.patch('/<tag>/enable')
	def enable_tag(tag:str|int):
		"""Attiva un tag."""

		try: tag = int(tag)
		except ValueError: pass

		if tag not in core.tags:
			abort(400, f"Il tag '{tag}' non esiste.")
		
		core.tags.enable(tag)
		
		return {'message': f"Tag '{tag}' attivato."}

	@route.patch('/<tag>/disable')
	def disable_tag(tag:str|int):
		"""Disattiva un tag."""

		try: tag = int(tag)
		except ValueError: pass

		if tag not in core.tags:
			abort(400, f"Il tag '{tag}' non esiste.")
		
		core.tags.disable(tag)

		return {'message': f"Tag '{tag}' disattivato."}

	return route