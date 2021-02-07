#!/usr/bin/python3

import animeworld as aw
import requests
import os
import re
import json
import schedule
import time
import shutil
import threading
from app import app

SONARR_URL = os.getenv('SONARR_URL') # Indirizzo ip + porta di sonarr
API_KEY = os.getenv('API_KEY') # Chiave api di sonarr
CHAT_ID = os.getenv('CHAT_ID') # telegramm
BOT_TOKEN = os.getenv('BOT_TOKEN') # telegramm

SCHEDULE_MINUTES = 30 # Ripetizione

WARNC='\033[93m' #GIALLO
ALERTC='\033[91m' # ROSSO
ERRORC='\033[4;3;91m' # ROSSO
TITLEC='\033[1;94m' # BLU
SEPARC='\033[90m' # GRIGIO
DIVIDC='\033[1;90m' # GRIGIO
OKC='\033[92m' # VERDE
NC='\033[0m' # Ripristino


start = r"""{color}┌------------------------------------{time}------------------------------------┐
{color}|                 _                _____                      _                 _            |
{color}|     /\         (_)              |  __ \                    | |               | |           |
{color}|    /  \   _ __  _ _ __ ___   ___| |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __  |
{color}|   / /\ \ | '_ \| | '_ ` _ \ / _ \ |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__| |
{color}|  / ____ \| | | | | | | | | |  __/ |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |    |
{color}| /_/    \_\_| |_|_|_| |_| |_|\___|_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|    |
{color}|                                                                                            |
{color}└--------------------------------------------------------------------------------------------┘{nc}
""".format(time=time.strftime('%d %b %Y %H:%M:%S'), color=TITLEC, nc=NC)


def main():
	print(start)

	if SONARR_URL == None:
		print("✖️ Variabile d'ambinete '𝙎𝙊𝙉𝘼𝙍𝙍_𝙐𝙍𝙇' non inserita.")
	else:
		print("✔ 𝙎𝙊𝙉𝘼𝙍𝙍_𝙐𝙍𝙇: {}".format(SONARR_URL))
	if API_KEY == None:
		print("✖️ Variabile d'ambinete '𝘼𝙋𝙄_𝙆𝙀𝙔' non inserita.")
	else:
		print("✔ 𝘼𝙋𝙄_𝙆𝙀𝙔: {}".format(API_KEY))
	if CHAT_ID == None:
		print("✖️ Variabile d'ambinete '𝘾𝙃𝘼𝙏_𝙄𝘿' non inserita.")
	else:
		print("✔ 𝘾𝙃𝘼𝙏_𝙄𝘿: {}".format(CHAT_ID))
	if BOT_TOKEN == None:
		print("✖️ Variabile d'ambinete '𝘽𝙊𝙏_𝙏𝙊𝙆𝙀𝙉' non inserita.")
	else:
		print("✔ 𝘽𝙊𝙏_𝙏𝙊𝙆𝙀𝙉: {}".format(BOT_TOKEN))

	if SONARR_URL != None and API_KEY !=None:
		print(f"\n{OKC}☑️ Le variabili d'ambiente sono state inserite correttamente.{NC}\n")

		print("\nAVVIO SERVER")
		job_thread = threading.Thread(target=server)
		job_thread.start()

		time.sleep(1)

		job() # Fa una prima esecuzione e poi lo imposta per la ripetizione periodica
		schedule.every(SCHEDULE_MINUTES).minutes.do(run_threaded, job)

def server():
	app.run(debug=False, host='0.0.0.0')		

def run_threaded(job_func):
	job_thread = threading.Thread(target=job_func)
	job_thread.start()
	

def job():
	divider = f"{DIVIDC}- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - {NC}"
	
	print("\n{color}╭-----------------------------------「{time}」-----------------------------------╮{nc}\n".format(time=time.strftime("%d %b %Y %H:%M:%S"), color=SEPARC, nc=NC))

	raw_series = get_missing_episodes()
	if len(raw_series)!=0:
		series = converting(raw_series)

		for info in series:
			print("\n", divider)

			try:
				print("🔎 Ricerca anime '{}'.".format(info["SonarrTitle"]))
				anime = [aw.Anime(link=x) for x in info["AnimeWorldLinks"]]

				print("🔎 Ricerca degli episodi per '{}'.".format(info["SonarrTitle"]))
				epsArr = [x.getEpisodes() for x in anime] # array di episodi da accorpare
				episodi = fixEps(epsArr)

				print("⚙️ Verifica se l'episodio 𝐒{}𝐄{} è disponibile.".format(info["season"], info["episode"]))
				ep = None
				for episodio in episodi:
					if episodio.number == str(info["episode"]):
						ep = episodio
						print("✔️ L'episodio è disponibile.")
						break
				else:
					print("✖️ L'episodio NON è ancora uscito.")

				if ep != None: # Se l'episodio è disponibile
					print("⏳ Download episodio 𝐒{}𝐄{}.".format(info["season"], info["episode"]))
					title = f'{info["SonarrTitle"]} - S{info["season"]}E{info["episode"]}'
					if ep.number == str(info["episode"]):
						fileLink = ep.links[0]
						title = fileLink.sanitize(title) # Sanitizza il titolo
						if fileLink.download(title): 
							print("✔️ Dowload Completato.")

					print("⏳ Spostamento episodio 𝐒{}𝐄{} in {}.".format(info["season"], info["episode"], info["path"]))
					if move_file(title, info["path"]): 
						print("✔️ Episodio spostato.")

					print("⏳ Ricaricando la serie '{}'.".format(info["SonarrTitle"]))
					RescanSerie(info["seriesId"])

					time.sleep(1)

					print("⏳ Rinominando l'episodio.")
					RenameSerie(info["seriesId"])

					if CHAT_ID != None or BOT_TOKEN != None:
						print("✉️ Inviando il messaggio via telegram.")
						send_message(info)

			except aw.AnimeNotAvailable as info:
				print(f"⚠️ {info}")
			except aw.ServerNotSupported as warning:
				print(f"{WARNC}🆆🅰🆁🅽🅸🅽🅶: {warning}{NC}")
			except aw.DeprecatedLibrary as dev:
				print(f"{ALERTC}🅰🅻🅴🆁🆃: {dev}{NC}")
			except Exception as error:
				print(f"{ERRORC}🅴🆁🆁🅾🆁: {error}{NC}")
			finally:
				print(divider, "\n")

	else:
		print("\nNon c'è nessun episodio da cercare.\n")

	nextStart = time.strftime("%d %b %Y %H:%M:%S", time.localtime(time.time() + SCHEDULE_MINUTES*60))
	print("\n{color}╰-----------------------------------「{time}」-----------------------------------╯{nc}\n".format(time=nextStart, color=SEPARC, nc=NC))

def fixEps(epsArr): # accorpa 2 o più serie di animeworld
	up = 0 # numero da aggiungere per rendere consecutivi gli episodi di varie stagioni
	ret = []

	for eps in epsArr:
		for ep in eps:
			ep.number = str(int(ep.number) + up)
			ret.append(ep)
		up += int(eps[-1].number)

	return ret


def converting(series):
	json_location = "/script/json/table.json"

	if not os.path.exists(json_location):
		raise Exception("Il file table.json non esiste.")

	f = open(json_location, 'r')
	table = json.loads(f.read())
	f.close()

	res = []

	for anime in series:
		for row in table:
			if row["title"] == anime["SonarrTitle"]:
				if str(anime["season"]) in row["seasons"].keys():
					anime["AnimeWorldLinks"] = list(row["seasons"][str(anime["season"])])
					res.append(anime)
					break
		else:

			print("❌ La 𝘴𝘵𝘢𝘨𝘪𝘰𝘯𝘦 {} della 𝘴𝘦𝘳𝘪𝘦 '{}' non esiste nella 𝗧𝗮𝗯𝗲𝗹𝗹𝗮 𝗗𝗶 𝗖𝗼𝗻𝘃𝗲𝗿𝘀𝗶𝗼𝗻𝗲.".format(anime["season"], anime["SonarrTitle"]))

	return res

def move_file(title, path):
	
	file = title
	if os.path.isfile(file+'.mp4'):
		file = file + '.mp4'
	elif os.path.isfile(file+'.mkv'):
		file = file + '.mkv'
	else:
		return False

	# destinationPath = os.fspath(path)
	path = path.replace('\\', '/')
	destinationPath = re.sub(r"\w:", "", path)
	currentPath = os.getcwd()

	source = os.path.join(currentPath, file)
	destination = os.path.join(destinationPath, file)

	print(destinationPath)

	if not os.path.exists(destinationPath):
		os.makedirs(destinationPath)
		print(f"⚠️ La cartella {destinationPath} è stata creata.")

	shutil.move(source, destination)
	return True

#### Sonarr ############################################################################################################

def get_missing_episodes():
	series = []
	endpoint = "wanted/missing"
	page = 0

	while True:
		page += 1
		res = requests.get("{}/api/{}?apikey={}&sortKey=airDateUtc&page={}".format(SONARR_URL, endpoint, API_KEY, page))
		result = res.json()

		# f = open("res.json", 'w')
		# f.write(json.dumps(result, indent=4))
		# f.close()

		if len(result["records"]) == 0: 
			break

		for serie in result["records"]:
			info = {}
			info["seriesId"] = serie["seriesId"]
			info["SonarrTitle"] = serie["series"]["title"]
			info["AnimeWorldLinks"] = []    # season 1 di sonarr corrisponde a più season di AnimeWorld
			info["season"] = int(serie["seasonNumber"])
			info["episode"] = int(serie["episodeNumber"])
			info["episodeTitle"] = serie["title"]
			info["path"] = serie["series"]["path"]

			series.append(info)

	return series

def getMaxEpisode(serieId, season):
	endpoint = f"series/{serieId}"
	res = requests.get("{}/api/{}?apikey={}&sortKey=airDateUtc".format(SONARR_URL, endpoint, API_KEY))
	result = res.json()

	for stagione in result["seasons"]:
		if stagione["seasonNumber"] == season:
			return stagione["statistics"]["totalEpisodeCount"]

def RescanSerie(seriesId):
	endpoint = "command"
	url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
	data = {
		"name": "RescanSeries",
		"seriesId": seriesId
	}
	requests.post(url, json=data)

def RenameSerie(seriesId):
	endpoint = "command"
	url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
	data = {
		"name": "RenameSeries",
		"seriesId": seriesId
	}
	requests.post(url, json=data)

#### Telegram ###########################################################################################################

def send_message(info):
	text = "*Episode Dowloaded*\n{title} - {season}x{episode} - {episodeTitle}".format(title=info["SonarrTitle"], season=str(info["season"]), episode=str(info["episode"]), episodeTitle=info["episodeTitle"])

	url ="https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(BOT_TOKEN, text, CHAT_ID)
	requests.get(url)

if __name__ == '__main__':
	main()
	while True:
		schedule.run_pending()
		time.sleep(1)

### ERRORI ####################################
