from ...backend import Core

from apiflask import APIBlueprint, abort, fields

def Tags(core:Core) -> APIBlueprint:

	route = APIBlueprint('tags', __name__, url_prefix='/tags', tag='Tags')

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

	return route