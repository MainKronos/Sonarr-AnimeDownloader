import time
from flask import request, Response
import sys, os, json

from .app import app
from utility import Table, Settings, Connections
from constants import SONARR_URL, API_KEY


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
	
@app.route('/api/connections', methods=['GET'])
def getConnections():

	connections = Connections.data
	for conn in connections:
		file = os.path.join("connections", conn["script"])
		if os.path.isfile(file):
			conn["valid"] = True
		else:
			conn["valid"] = False

	return Response(
		mimetype='application/json',
		status=200,
		response=json.dumps({
			"error": False,
			"data": connections
		})
	)

@app.route('/api/connections/toggle', methods=['POST'])
def toggleConnection():
	data = request.json

	name = data["name"]

	log = Connections.toggle(name)

	return Response(
		mimetype='application/json',
		status=200,
		response=json.dumps({
			"error": False,
			"data": log
		})
	)

@app.route('/api/connections/remove', methods=['POST'])
def removeConnection():
	data = request.json

	name = data["name"]

	log = Connections.remove(name)

	return Response(
		mimetype='application/json',
		status=200,
		response=json.dumps({
			"error": False,
			"data": log
		})
	)

@app.route('/api/connections/add', methods=['POST'])
def addConnection():
	data = request.json

	name = data["name"]
	script = data["script"]
	active = data["active"]

	log = Connections.add(name, script, active)

	return Response(
		mimetype='application/json',
		status=200,
		response=json.dumps({
			"error": False,
			"data": log
		})
	)


# IMPORT / EXPORT 
@app.route('/ie/table', methods=['GET', 'POST'])
def ieTable():
	if request.method == 'GET':
		return Response(
			json.dumps(Table.data, indent=4),
			mimetype="text/plain",
			headers={"Content-disposition":"attachment; filename=table.json"}
		)
	else:
		uploaded_file = request.files['file']
		if uploaded_file.filename != '':
			data = uploaded_file.read()
			check = True
			try:
				check = Table.write(json.loads(data.decode('utf-8')))
			except json.decoder.JSONDecodeError:
				check = False
			
			
			return Response(
				mimetype='application/json',
				status=200,
				response=json.dumps({
					"error": False if check else f"Table invalida."
				})
	)

@app.route('/ie/settings', methods=['GET', 'POST'])
def ieSettings():
	if request.method == 'GET':
		return Response(
			json.dumps(Settings.data, indent=4),
			mimetype="text/plain",
			headers={"Content-disposition":"attachment; filename=settings.json"}
		)
	else:
		uploaded_file = request.files['file']
		if uploaded_file.filename != '':
			data = uploaded_file.read()
			check = True
			try:
				check = Settings.write(json.loads(data.decode('utf-8')))
			except json.decoder.JSONDecodeError:
				check = False
			
			
			return Response(
				mimetype='application/json',
				status=200,
				response=json.dumps({
					"error": False if check else f"Settings invalide."
				})
	)

@app.route('/ie/log', methods=['GET'])
def ieLog():

	data = open("log.log", 'r', encoding='utf-8').read()
	data = data.replace(SONARR_URL, '█'*len(SONARR_URL)).replace(API_KEY, '█'*len(API_KEY))

	return Response(
		data,
		mimetype="text/plain",
		headers={"Content-disposition":"attachment; filename=log.log"}
	)

@app.route('/ie/connections', methods=['GET', 'POST'])
def ieConnections():
	if request.method == 'GET':
		return Response(
			json.dumps(Connections.data, indent=4),
			mimetype="text/plain",
			headers={"Content-disposition":"attachment; filename=connections.json"}
		)
	else:
		uploaded_file = request.files['file']
		if uploaded_file.filename != '':
			data = uploaded_file.read()

			check = True
			try:
				check = Connections.write(json.loads(data.decode('utf-8')))
			except json.decoder.JSONDecodeError:
				check = False

			
			return Response(
				mimetype='application/json',
				status=200,
				response=json.dumps({
					"error": False if check else f"Connections invalide."
				})
	)