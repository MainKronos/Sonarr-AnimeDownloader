from flask import *
import sys

from .app import app
from utility import Table, Settings


@app.route('/api/table', methods=['GET'])
def getTable():
	return Response(
		mimetype='application/json',
		status=200,
		response=json.dumps({
			"error": False,
			"data": Table.data
		})
	)

@app.route('/api/table/add', methods=['POST'])
def addData():
	data = request.json
	title = data["title"]
	season = data["season"]
	links = data["links"]
	absolute = data["absolute"]

	log = Table.append({
		"title": title,
		"season": season,
		"absolute": absolute,
		"links": links
	})

	return Response(
		mimetype='application/json',
		status=200,
		response=json.dumps({
			"error": False,
			"data": log
		})
	)

@app.route('/api/table/remove', methods=['POST'])
def removeData():
	data = request.json
	title = data["title"]
	season = data["season"] if "season" in data else None
	link = data["link"] if "link" in data else None

	log = Table.remove(
		title,
		season,
		link
	)

	return Response(
		mimetype='application/json',
		status=200,
		response=json.dumps({
			"error": False,
			"data": log
		})
	)

@app.route('/api/table/edit', methods=['POST'])
def editData():

	data = request.json
	title = data["title"]
	season = data["season"] if "season" in data else None
	link = data["link"] if "link" in data else None

	log = Table.edit(
		title,
		season,
		link
	)

	return Response(
		mimetype='application/json',
		status=200,
		response=json.dumps({
			"error": False,
			"data": log
		})
	)

@app.route('/api/settings', methods=['GET'])
def getSettings():
	return Response(
		mimetype='application/json',
		status=200,
		response=json.dumps({
			"error": False,
			"data": Settings.data
		})
	)

@app.route('/api/settings', methods=['POST'])
def updateSettings():
	data = request.json

	AutoBind = data["AutoBind"]
	LogLevel = data["LogLevel"]
	MoveEp = data["MoveEp"]
	RenameEp = data["RenameEp"]
	ScanDelay = data["ScanDelay"]

	log = Settings.update(AutoBind, LogLevel, MoveEp, RenameEp, ScanDelay)

	return Response(
		mimetype='application/json',
		status=200,
		response=json.dumps({
			"error": False,
			"data": log
		})
	)

@app.route('/api/log', methods=['GET'])
@app.route('/api/log/<row>', methods=['GET'])
def getLog(row:int=0):
	rows = 100
	row = int(row)

	return Response(
		mimetype='application/json',
		status=200,
		response=json.dumps({
			"error": False,
			"data": [
				x for x in (open("log.log", 'r', encoding='utf-8').readlines())
			][ -(rows + row) :]
			# ][ -100 :  - 1]
		})
	)
	
