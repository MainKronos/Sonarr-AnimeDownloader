import re
import json
import os
from flask import *
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

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
		"season": request.form['season'],
		"link": request.form['link']
	}
	appendAnime(data)
	return redirect(url_for('index'))

@app.route('/delete_anime', methods=['POST']) # Per aggiungere un anime
def delete_anime():
	res = request.form
	# print(res, flush=True)
	deleteAnime(res['delete_anime'])

	return redirect(url_for('index'))

@app.route('/index')
@app.route('/')
def index():

	anime = readData()
	env = getmyenv()
	return render_template('index.html', infos=anime, env=env)



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

def appendAnime(data):
	def myOrder(serieInfo):
		return serieInfo["title"]

	table = readData()

	for anime in table:
		if data["title"] == anime["title"]: # Se esiste già l'anime nella tabella

			if data["season"] in anime["seasons"]: # Se esiste già la stagione
				anime["seasons"][data["season"]].append(data["link"]) # aggiunge un'altro link
				# print(f"\n-> È stata aggiunto un altro link per la stagione {season} della serie {SonarrTitle}.")
			else:
				anime["seasons"][data["season"]] = [data["link"]] # inizializza una nuova stagione
				# print(f"\n-> È stata aggiunta la stagione {season} per la serie {SonarrTitle}.")

			break
	else: # se non è stato trovato nessun anime
		table.append({
			"title": data["title"],
			"seasons": {data["season"]: [data["link"]]}
		})
		# print(f"\n-> È stata aggiunta la serie {SonarrTitle}.")

	table.sort(key=myOrder)
	writeData(table)


### getenv

def getmyenv():
	env = {}

	env["ANIME_PATH"] = os.getenv('ANIME_PATH') # cartella dove si trovano gli anime
	env["SONARR_URL"] = os.getenv('SONARR_URL') # Indirizzo ip + porta di sonarr
	env["API_KEY"] = os.getenv('API_KEY') # Chiave api di sonarr
	env["CHAT_ID"] = os.getenv('CHAT_ID') # telegramm
	env["BOT_TOKEN"] = os.getenv('BOT_TOKEN') # telegramm

	return env