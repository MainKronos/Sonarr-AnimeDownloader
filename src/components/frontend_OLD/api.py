import time
from flask import Flask, Response, request
import sys, os, json

from ..backend import Core

def loadAPI(app:Flask):

	core:Core = app.config['CORE']

	@app.route('/api/rescan', methods=['GET'])
	def rescan():
		result = core.wakeUp()
		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": result,
				"data": "Rescan schedulato." if result else "Errore in fase di rescan"
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)

	@app.route('/api/table', methods=['GET'])
	def getTable():
		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": core.table.getData()
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)

	@app.route('/api/table/add', methods=['POST'])
	def addData():
		data = request.json
		title = data["title"]
		season = data["season"]
		links = data["links"]
		absolute = data["absolute"]

		core.table.appendSerie(title, absolute)
		core.table.appendUrls(title, season, links)

		log = "Informazioni aggiunte."

		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": log
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)

	@app.route('/api/table/remove', methods=['POST'])
	def removeData():
		data = request.json
		title = data["title"]
		season = data["season"] if "season" in data else None
		link = data["link"] if "link" in data else None

		log = ""

		try:
			if link:
				core.table.removeUrl(title, season, link)
				log = "Url rimosso."
			elif season:
				core.table.removeSeason(title, season)
				log = f"Stagione {season} rimossa."
			else:
				core.table.removeSerie(title)
				log = f"Serie {title} rimossa."
		except KeyError as e:
			log = str(e)

		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": log
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)

	@app.route('/api/table/edit', methods=['POST'])
	def editData():

		data = request.json
		title = data["title"]
		season = data["season"] if "season" in data else None
		link = data["link"] if "link" in data else None

		log = ""
		try:
			if link:
				if core.table.renameUrl(title, season, link[0], link[1]):
					log = "Url modificato."
				else:
					log = "Errore nella modifica dell'url."
			elif season:
				if core.table.renameSeason(title, season[0], season[1]):
					log = f"Stagione {season[0]} modificata."
				else:
					log = "Errore nella modifica della stagione."
			else:
				if core.table.renameSerie(title[0], title[1]):
					log = f"Serie {title} modificata."
				else:
					log = "Errore nella modifica della serie." 
		except KeyError as e:
			log = str(e)

		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": log
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)

	@app.route('/api/settings', methods=['GET'])
	def getSettings():
		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": core.settings.getData()
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)

	@app.route('/api/settings', methods=['POST'])
	def updateSettings():
		data = request.json

		log = "ERRORE"
		if data["AutoBind"]:
			core.settings["AutoBind"] = data["AutoBind"]
			log = "Auto Ricerca Link aggiornato."
		elif data["LogLevel"]:
			core.settings["LogLevel"] = data["LogLevel"]
			log = "Livello del Log aggiornato."
		elif data["MoveEp"]:
			core.settings["MoveEp"] = data["MoveEp"]
			log = "Sposta Episodi aggiornato."
		elif data["RenameEp"]:
			core.settings["RenameEp"] = data["RenameEp"]
			log = "Rinomina Episodi aggiornato."
		elif data["ScanDelay"]:
			core.settings["ScanDelay"] = data["ScanDelay"]
			log = "Intervallo Scan aggiornato."
		elif data["TagsMode"]:
			core.settings["TagsMode"] = data["TagsMode"]
			log = "Modalità tags aggiornata."

		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": log
			}),
			headers={"Access-Control-Allow-Origin": "*"}
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
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)
		
	@app.route('/api/connections', methods=['GET'])
	def getConnections():

		connections = core.connections_db.getData()
		for conn in connections:
			if core.connections_db.getPath(conn['name']).is_file():
				conn["valid"] = True
			else:
				conn["valid"] = False

		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": connections
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)

	@app.route('/api/connections/toggle', methods=['POST'])
	def toggleConnection():
		data = request.json

		log = ""
		try:
			res = core.connections_db.toggle(data["name"])
			log = f"La Connection {data['name']} è stata {'attivata' if res else 'disattivata'}."
		except KeyError:
			log = f"Non è stato trovato nessuna Connection con il nome {data['name']}."

		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": log
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)

	@app.route('/api/connections/remove', methods=['POST'])
	def removeConnection():
		data = request.json

		log = ""
		try:
			del core.connections_db[data["name"]]
			log = f"La Connection {data['name']} è stata rimossa."
		except KeyError:
			log = f"Non è stato trovato nessuna Connection con il nome {data['name']}."

		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": log
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)

	@app.route('/api/connections/add', methods=['POST'])
	def addConnection():
		data = request.json

		log = ""
		try:
			core.connections_db.append(data["name"], data["script"], data["active"])
			log = f"La Connection {data['name']} è stata aggiunta."
		except ValueError as e:
			log = str(e)
		except FileNotFoundError:
			log = f"il file {data['script']} non esiste."

		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": log
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)

	#  TAGS
		
	@app.route('/api/tags', methods=['GET'])
	def getTags():
		
		tags = core.tags.getData()
		for tag in tags:
			tag["valid"] = True

		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": tags
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)
		
	@app.route('/api/tags/toggle', methods=['POST'])
	def toggleTag():
		data = request.json

		tag_id = data["id"]

		log = ""
		try:
			res = core.tags.toggle(data["name"])
			log = f"Il tag {data['name']} è stato {'attivato' if res else 'disattivato'}."
		except KeyError:
			log = f"Non è stato trovato nessun Tag con il nome {data['name']}."


		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": log
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)

	@app.route('/api/tags/remove', methods=['POST'])
	def removeTag():
		data = request.json

		tag_id = data["id"]
		name = data["name"]

		log = ""
		try:
			del core.tags[name]
			log = f"Il tag {data['name']} è stato rimosso."
		except KeyError:
			log = f"Non è stato trovato nessun Tag con il nome {data['name']}."

		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": log
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)

	@app.route('/api/tags/add', methods=['POST'])
	def addTag():
		data = request.json

		name = data["name"]
		active = data["active"]

		res = core.sonarr.tags()
		res.raise_for_status()

		sonarr_tag = next(filter(lambda x:x["label"] == name, res.json()), None)

		log = ""
		if sonarr_tag:
			tag_id = sonarr_tag["id"]
			try:
				core.tags.append(tag_id, name, active)
				log = f"Il tag {name} è stato aggiunto."
			except ValueError as e:
				log = str(e)
		else:
			log = f"Il Tag {name} non esiste su Sonarr."


		return Response(
			mimetype='application/json',
			status=200,
			response=json.dumps({
				"error": False,
				"data": log
			}),
			headers={"Access-Control-Allow-Origin": "*"}
		)

	# IMPORT / EXPORT 
	@app.route('/ie/table', methods=['GET', 'POST'])
	def ieTable():
		if request.method == 'GET':
			return Response(
				json.dumps(core.table.getData(), indent=4),
				mimetype="text/plain",
				headers={"Content-disposition":"attachment; filename=table.json", "Access-Control-Allow-Origin": "*"},
			)
		else:
			uploaded_file = request.files['file']
			if uploaded_file.filename != '':
				data = uploaded_file.read()
				check = True
				try:
					check = core.table.setData(json.loads(data.decode('utf-8')))
				except json.decoder.JSONDecodeError:
					check = False
				
				return Response(
					mimetype='application/json',
					status=200,
					response=json.dumps({
						"error": False if check else f"Table invalida."
					}),
					headers={"Access-Control-Allow-Origin": "*"}
				)

	@app.route('/ie/settings', methods=['GET', 'POST'])
	def ieSettings():
		if request.method == 'GET':
			return Response(
				json.dumps(core.settings.getData(), indent=4),
				mimetype="text/plain",
				headers={"Content-disposition":"attachment; filename=settings.json", "Access-Control-Allow-Origin": "*"}
			)
		else:
			uploaded_file = request.files['file']
			if uploaded_file.filename != '':
				data = uploaded_file.read()
				check = True
				try:
					check = core.settings.setData(json.loads(data.decode('utf-8')))
				except json.decoder.JSONDecodeError:
					check = False
				
				return Response(
					mimetype='application/json',
					status=200,
					response=json.dumps({
						"error": False if check else f"Settings invalide."
					}),
					headers={"Access-Control-Allow-Origin": "*"}
				)

	@app.route('/ie/log', methods=['GET'])
	def ieLog():

		SONARR_URL = core.sonarr.url
		API_KEY = core.sonarr.api_key

		data = open("log.log", 'r', encoding='utf-8').read()
		data = data.replace(SONARR_URL, '█'*len(SONARR_URL)).replace(API_KEY, '█'*len(API_KEY))

		return Response(
			data,
			mimetype="text/plain",
			headers={"Content-disposition":"attachment; filename=log.log", "Access-Control-Allow-Origin": "*"}
		)

	@app.route('/ie/connections', methods=['GET', 'POST'])
	def ieConnections():
		if request.method == 'GET':
			return Response(
				json.dumps(core.connections_db.getData(), indent=4),
				mimetype="text/plain",
				headers={"Content-disposition":"attachment; filename=connections.json", "Access-Control-Allow-Origin": "*"}
			)
		else:
			uploaded_file = request.files['file']
			if uploaded_file.filename != '':
				data = uploaded_file.read()

				check = True
				try:
					check = core.connections_db.setData(json.loads(data.decode('utf-8')))
				except json.decoder.JSONDecodeError:
					check = False
				
				return Response(
					mimetype='application/json',
					status=200,
					response=json.dumps({
						"error": False if check else f"Connections invalide."
					}),
					headers={"Access-Control-Allow-Origin": "*"}
				)

	@app.route('/ie/tags', methods=['GET', 'POST'])
	def ieTags():
		if request.method == 'GET':
			return Response(
				json.dumps(core.tags.getData(), indent=4),
				mimetype="text/plain",
				headers={"Content-disposition":"attachment; filename=tags.json", "Access-Control-Allow-Origin": "*"}
			)
		else:
			uploaded_file = request.files['file']
			if uploaded_file.filename != '':
				data = uploaded_file.read()

				check = True
				try:
					check = core.tags.setData(json.loads(data.decode('utf-8')))
				except json.decoder.JSONDecodeError:
					check = False
				
				return Response(
					mimetype='application/json',
					status=200,
					response=json.dumps({
						"error": False if check else f"Tag invalidi."
					}),
					headers={"Access-Control-Allow-Origin": "*"}
				)