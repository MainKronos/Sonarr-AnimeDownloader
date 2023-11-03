from ...backend import Core

from apiflask import APIBlueprint, abort, fields

def Settings(core:Core) -> APIBlueprint:

	route = APIBlueprint('settings', __name__, url_prefix='/settings', tag='Settings')

	@route.get('/')
	def get_settings():
		"""Restituisce le impostazioni."""

		return core.settings.getData()
	
	@route.patch('/<setting>')
	@route.input({'value': fields.Raw()})
	def edit_settings(setting:str, json_data:dict):
		"""Modifica un impostazione."""
		
		if setting not in core.settings:
			abort(400, f"L'impostazione '{setting}' non esiste.")

		core.settings[setting] = json_data['value']

		return {'message': f"Impostazione '{setting}' aggiornata."}

	return route
