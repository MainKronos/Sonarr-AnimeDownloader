import re
import json
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

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['POST', 'GET'])
def index():

	if request.method == 'POST':
		res = request.form
		data = {
			"title": request.form['title'],
			"season": request.form['season'],
			"link": request.form['link']
		}
		writeData(data)
		return redirect(url_for('index'))
	else:
		anime = readData()
		return render_template('index.html', infos=anime)



#######

def readData():
	with open('json/table.json' , 'r') as f:
		return json.loads(f.read())

def writeData(data):
	def myOrder(serieInfo):
		return serieInfo["title"]

	# data = {
	# 	"title":"",
	# 	"season": "",
	# 	"link": ""
	# }

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

	table.sort(key=myOrder) # Riordina la tabella in ordine alfabetico

	f = open("json/table.json", 'w')
	f.write(json.dumps(table, indent=4))
	f.close()
	return table