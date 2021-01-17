#!/usr/bin/python3

import animeworld as aw
import requests
import os
import re
import json
import schedule
import time
import sys

ANIME_PATH = os.getenv('ANIME_PATH') # cartella dove si trovano gli anime
SONARR_URL = os.getenv('SONARR_URL') # Indirizzo ip + porta di sonarr
API_KEY = os.getenv('API_KEY') # Chiave api di sonarr
CHAT_ID = os.getenv('CHAT_ID') # telegramm
BOT_TOKEN = os.getenv('BOT_TOKEN') # telegramm

SCHEDULE_MINUTES = 30

###### supported provider
Streamtape = "Streamtape"
YouTube = "YouTube"
Beta_Server = "Beta Server"
VVVVID = "VVVVID"
AnimeWorld_Server = "AnimeWorld Server"
#####


start = f"┌------------------------------------{time.strftime('%d %b %Y %H:%M:%S')}------------------------------------┐" + r"""
|                 _                _____                      _                 _            |
|     /\         (_)              |  __ \                    | |               | |           |
|    /  \   _ __  _ _ __ ___   ___| |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __  |
|   / /\ \ | '_ \| | '_ ` _ \ / _ \ |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__| |
|  / ____ \| | | | | | | | | |  __/ |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |    |
| /_/    \_\_| |_|_|_| |_| |_|\___|_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|    |
|                                                                                            |
└--------------------------------------------------------------------------------------------┘
""".format()


def main():
	print(start)

	if ANIME_PATH == None:
		print("✖️ Variabile d'ambinete '𝘼𝙉𝙄𝙈𝙀_𝙋𝘼𝙏𝙃' non inserita.")
	else:
		print("✔ 𝘼𝙉𝙄𝙈𝙀_𝙋𝘼𝙏𝙃: {}".format(ANIME_PATH))
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

	if ANIME_PATH != None or SONARR_URL != None or API_KEY !=None:
		print("\n☑️ Le variabili d'ambiente sono state inserite correttamente.\n")
		job() # Fa una prima esecuzione e poi lo imposta per la ripetizione periodica
		schedule.every(SCHEDULE_MINUTES).minutes.do(job)	

def job():
	divider = "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
	
	print("\n╭-----------------------------------「{}」-----------------------------------╮\n".format(time.strftime("%d %b %Y %H:%M:%S")))

	raw_series = get_missing_episodes()
	if len(raw_series)!=0:
		series = converting(raw_series)

		for info in series:
			print("\n", divider)

			try:
				print("🔎 Ricerca anime {} 𝐒{}𝐄{}.".format(info["SonarrTitle"], str(info["season"]), str(info["episode"])))
				anime = aw.Anime(link=info["AnimeWorldLinks"][0])

				print("🔎 Ricerca degli episodi per {} 𝐒{}𝐄{}.".format(info["SonarrTitle"], str(info["season"]), str(info["episode"])))
				episodi = anime.getEpisodes()

				print("⏳ Download episodio 𝐒{}𝐄{}.".format(str(info["season"]), str(info["episode"])))
				title = info["episodeTitle"]
				for ep in episodi:
					if ep.number == str(info["episode"]):
						fileLink = ep.links[0]
						title = fileLink.sanitize(title)
						if fileLink.download(title): 
							print("✔️ Dowload Completato.")

				print("⏳ Spostamento episodio 𝐒{}𝐄{}.".format(str(info["season"]), str(info["episode"])))
				if move_file(title, info["path"]): 
					print("✔️ Episodio spostato.".format(file))

				print("⏳ Ricaricando la serie {}.".format(info["season"]))
				RescanSerie(info["seriesId"])

				print("⏳ Rinominamento episodio 𝐒{}𝐄{}.".format(str(info["season"]), str(info["episode"])))
				RenameSerie(info["seriesId"])

				if CHAT_ID != None or BOT_TOKEN != None:
					print("📧 Inviando il messaggio via telegram.")
					send_message(info)

			except Exception as ex:
				print(f"🅴🆁🆁🅾🆁🅴: {ex}")
			finally:
				print(divider, "\n")

	else:
		print("\nNon c'è nessun episodio da cercare.\n")

	nextStart = time.strftime("%d %b %Y %H:%M:%S", time.localtime(time.time() + SCHEDULE_MINUTES*60))
	print("\n╰-----------------------------------「{}」-----------------------------------╯\n".format(nextStart))


def getSeriesID(series):
	ids = []
	for info in series:
		ids.append(info["seriesId"])
	return ids

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

			print("La 𝘴𝘵𝘢𝘨𝘪𝘰𝘯𝘦 {} della 𝘴𝘦𝘳𝘪𝘦 '{}' non esiste nella tabella per le conversioni.".format(anime["season"], anime["SonarrTitle"]))

	return res

### AnimeWorld #############################################################################################################


def move_file(title, path):
	
	file = title
	if os.path.isfile(file+'.mp4'):
		file = file + '.mp4'
	elif os.path.isfile(file+'.mkv'):
		file = file + '.mkv'
	else:
		return False

	destinationPath = path
	currentPath = os.getcwd()

	source = os.path.join(currentPath, file)
	destination = os.path.join(destinationPath, file)

	if not os.path.exists(destinationPath):
		os.makedirs(destinationPath)

	shutil.move(source, destination)
	return True

#### Sonarr ############################################################################################################

def get_missing_episodes():
	endpoint = "wanted/missing"
	res = requests.get("{}/api/{}?apikey={}&sortKey=airDateUtc".format(SONARR_URL, endpoint, API_KEY))
	result = res.json()

	# f = open("res.json", 'w')
	# f.write(json.dumps(result, indent=4))
	# f.close()

	series = []

	for serie in result["records"]:
		info = {}
		info["seriesId"] = serie["seriesId"]
		info["SonarrTitle"] = serie["series"]["title"]
		info["AnimeWorldLinks"] = []    # season 1 di sonarr corrisponde a più season di AnimeWorld
		info["season"] = int(serie["seasonNumber"])
		info["episode"] = int(serie["episodeNumber"])
		# info["absEpisode"] = int(serie["absoluteEpisodeNumber"])  # il numero assoluto dell'episodio
		# info["maxEpisode"] = getMaxEpisode(serieId=info["seriesId"], season=info["season"])
		info["episodeTitle"] = serie["title"]
		info["path"] = os.path.join(ANIME_PATH, serie["series"]["path"].split("/")[-1])

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