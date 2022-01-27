from configparser import ConfigParser
import re
import json
import os
from flask import *
import sys
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

LOG = None # variabile usata per inviare messaggi a schermo

@app.template_filter()
def msgSafe(msg):
	msg = re.sub(r"[^a-zA-Z]", "", msg)
	return msg

@app.route('/favicon.ico') 
def favicon(): 
    return redirect(url_for('static', filename='favicon.ico'), code=302)

@app.route('/append_anime', methods=['POST']) # Per aggiungere un anime
def append_anime():
	res = request.form
	data = {
		"title": request.form['title'],
		"season": "absolute",
		"absolute": ("absolute" in request.form),
		"links": request.form.getlist('link')
	}
	if not data["absolute"]:
		data["season"]= request.form['season']
	# print(data, file=sys.stderr)

	global LOG
	LOG = appendAnime(data)
	return redirect(url_for('index'))

@app.route('/delete_anime', methods=['POST']) # Per cancellare un anime
def delete_anime():
	res = request.form
	# print(res, flush=True)
	deleteAnime(res['delete_anime'])

	return redirect(url_for('index'))

@app.route('/edit_anime', methods=['POST']) # Per modificare un anime
def edit_anime():
	res = request.form
	# print(res, flush=True)
	editAnime(res['edit_anime'], res['input'])

	return redirect(url_for('index'))

@app.route('/settings')
def settings():
	setts = ReadSettings()
	env = getmyenv()
	return render_template('settings.html', settings=setts, env=env)

@app.route('/settings_update', methods=['POST'])
def settings_update():
	res = request.form
	settings = {
		"LogLevel": request.form.get("LogLevel"),
		"RenameEp": False if request.form.get("RenameEp") is None or request.form.get("MoveEp") is None else True,
		"MoveEp": False if request.form.get("MoveEp") is None else True,
		"ScanDalay": int(request.form.get("ScanDalay")),
		"AutoBind": False if request.form.get("AutoBind") is None else True
	}

	WriteSettings(settings)
	# print(request.form.get("RenameEp"), file=sys.stderr)
	# print(res, file=sys.stderr)
	return redirect(url_for('settings'))

@app.route('/index')
@app.route('/')
def index():
	log = get_log()
	anime = readData()
	env = getmyenv()
	return render_template('index.html', infos=anime, log=log, env=env)


@app.route('/get_logs')
@app.route('/get_logs/<rows>')
def get_logs(rows=100):

	return {'data': [x for x in (open("log.log").readlines())][-int(rows):99 - int(rows)]}

@app.route('/log')
def log():
	env = getmyenv()
	return render_template('log.html', env=env)

####### DATA

def readData():
	with open('json/table.json' , 'r') as f:
		return json.loads(f.read())

def writeData(table):
	f = open("json/table.json", 'w')
	f.write(json.dumps(table, indent=4))
	f.close()
	return table

def deleteAnime(title):

	table = readData()

	for anime in table:
		if anime["title"] == title:
			table.remove(anime)
			break

	writeData(table)

def editAnime(title, newTitle):
	table = readData()

	for anime in table:
		if anime["title"] == title:
			anime["title"] = newTitle
			break

	writeData(table)

def appendAnime(data):
	def myOrder(serieInfo):
		return serieInfo["title"]

	table = readData()
	log = None # In caso di errore viene segnalato a video


	for anime in table:
		if data["title"] == anime["title"]: # Se esiste già l'anime nella tabella
			if data["season"] in anime["seasons"]: # Se esiste già la stagione
				for link in data["links"]:
					if link not in anime["seasons"][data["season"]]: # Se il link non è già presente
						anime["seasons"][data["season"]].append(link)  # aggiunge un'altro link
						log = "Nuovo link aggiunto"
			else:
				if not anime["absolute"] and not data["absolute"]:  # Se la numerazione non è assoluta
					anime["seasons"][data["season"]] = list(data["links"]) # inizializza una nuova stagione
					log = f"Stagione {data['season']} di {data['title']} aggiunta"
				else:
					log = "ERRORE"	

			break
	else: # se non è stato trovato nessun anime
		table.append({
			"title": data["title"],
			"seasons": {data["season"]: data["links"]},
			"absolute": data["absolute"]
		})
		log = f"{data['title']} aggiunto"
		# print(f"\n-> È stata aggiunta la serie {SonarrTitle}.")

	table.sort(key=myOrder)
	writeData(table)
	return log

### getenv

def getmyenv():
	env = {}

	env["SONARR_URL"] = os.getenv('SONARR_URL') # Indirizzo ip + porta di sonarr
	env["API_KEY"] = os.getenv('API_KEY') # Chiave api di sonarr
	env["CHAT_ID"] = os.getenv('CHAT_ID') # telegramm
	env["BOT_TOKEN"] = os.getenv('BOT_TOKEN') # telegramm
	env["VERSION"] = os.getenv('VERSION') # versione

	return env


### Setting 

def ReadSettings():

	data = {
		"LogLevel": "DEBUG",
		"RenameEp": True,
		"MoveEp": True,
		"ScanDalay": 30,
		"AutoBind": False
	}

	json_location = "json/settings.json"
	updateFix = False

	settings = {}

	if os.path.exists(json_location):
		with open(json_location, 'r') as f:
			settings = json.loads(f.read())

		for info in data:
			if info not in settings:
				settings[info] = data[info]
				updateFix = True
	else:
		settings = data
		updateFix = True

	if updateFix:
		with open(json_location, 'w') as f:
			f.write(json.dumps(settings, indent='\t'))
	
	return settings


def WriteSettings(settings):
	json_location = "json/settings.json"
	with open(json_location, 'w') as f:
			f.write(json.dumps(settings, indent='\t'))

### OTHER

def get_log():
	global LOG
	log = LOG
	LOG = None
	return log


if __name__ == "__main__":
    app.run(debug=False, use_evalex=False, use_reloader=False, host='0.0.0.0')
