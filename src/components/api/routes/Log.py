from ...backend import Core

from apiflask import APIBlueprint
from flask import Response

def Log(core:Core) -> APIBlueprint:

	route = APIBlueprint('log', __name__, url_prefix='/log', tag='Log')
	
	@route.after_request
	def cors(res):
		res.headers['Access-Control-Allow-Origin'] = '*'
		res.headers['Access-Control-Allow-Headers'] = '*'
		res.headers['Access-Control-Allow-Methods'] = '*'
		return res
	
	@route.get('/')
	def get_log():
		"""Restituisce il log."""

		def generate():
			for row in reversed(open("log.log", 'rb').readlines()):
				yield row
		return Response(generate(), mimetype='text/plain')

	return route