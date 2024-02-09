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
	@route.get('/<page>')
	def get_log(page:int=0):
		"""Restituisce il log."""
		
		page = int(page)

		log = open("log.log", 'r', encoding='utf-8').readlines()
		rows = len(log)

		row_start = rows - ((page + 1) * 100)
		if row_start < 0: row_start = 0
		row_end = rows - (page * 100)
		if row_end < 0: return []

		return log[row_start:row_end]

	return route