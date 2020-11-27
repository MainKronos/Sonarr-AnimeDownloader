#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import os
import youtube_dl
import re
import json
import shutil
import schedule
import time
from clint.textui import progress
import sys

cookies = {}
# cookies = {'AWCookietest': 'cf18e136cadc69aaf3ee7ce302766ae3'}
HDR = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}

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


start = """
┌----------------------------------{}----------------------------------┐
|                 _                  _____                _                 _            |
|     /\\         (_)                |  __ \\              | |               | |           |
|    /  \\   _ __  _ _ __ ___   ___  | |  | | _____      _| | ___   __ _  __| | ___ _ __  |
|   / /\\ \\ | '_ \\| | '_ ` _ \\ / _ \\ | |  | |/ _ \\ \\ /\\ / / |/ _ \\ / _` |/ _` |/ _ \\ '__| |
|  / ____ \\| | | | | | | | | |  __/ | |__| | (_) \\ V  V /| | (_) | (_| | (_| |  __/ |    |
| /_/    \\_\\_| |_|_|_| |_| |_|\\___| |_____/ \\___/ \\_/\\_/ |_|\\___/ \\__,_|\\__,_|\\___|_|    |
|                                                                                        |
└----------------------------------------------------------------------------------------┘
""".format(time.strftime("%d %b %Y %H:%M:%S"))

divider = "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "


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
	print("\n╭---------------------------------「{}」---------------------------------╮\n".format(time.strftime("%d %b %Y %H:%M:%S")))

	try:
		series = get_missing_episodes()
		if len(series)!=0:
			seriesFull = converting(series)
			anime = AnimeWorld(seriesFull)
			if len(anime)!=0:
				animeUp = dowload_file(anime)
				move_file(animeUp)
				seriesIds = getSeriesID(animeUp)

				RescanSeries(seriesIds)
				time.sleep(10*len(seriesIds))
				RenameSeries(seriesIds)

				if CHAT_ID != None and BOT_TOKEN != None:
					send_message(anime)
		else:
			print("\nNon c'è nessun episodio da cercare.\n")
	except Exception as e:
		print("🅴🆁🆁🅾🆁🅴: {}".format(e))
	finally:
		nextStart = time.strftime("%d %b %Y %H:%M:%S", time.localtime(time.time() + SCHEDULE_MINUTES*60))
		print("\n╰---------------------------------「{}」---------------------------------╯\n".format(nextStart))

def getSeriesID(series):
	ids = []
	for info in series:
		ids.append(info["seriesId"])
	return ids

def converting(series):
	json_location = "/script/json/table.json"

	if not os.path.exists(json_location):
		f = open(json_location, 'w')
		f.write(json.dumps(list([]), indent=4))
		f.close()

	f = open(json_location, 'r')
	table = json.loads(f.read())
	f.close()
	seriesNew = [] 

	for info in series:
		for row in table:
			if row["Sonarr"]["title"] == info["SonarrTitle"] and row["Sonarr"]["season"] == info["season"]:
				info["AnimeWorldTitle"] = row["AnimeWorld"]["title"]
				seriesNew.append(info)
				break
		else:
			print("La 𝘴𝘵𝘢𝘨𝘪𝘰𝘯𝘦 {} della 𝘴𝘦𝘳𝘪𝘦 '{}' non esiste nella tabella per le conversioni.".format(info["season"], info["SonarrTitle"]))


	return seriesNew

### AnimeWorld #############################################################################################################

def AnimeWorld(series):
	seriesNew = []
	for info in series:
		print("\n", divider)

		anime_link = []
		episode_links = {}
		mp4_link = None
		external = False

		providers = {}

		### Get anime_link ###

		print("Ricerca anime link per {} 𝐒{}𝐄{}.".format(info["SonarrTitle"], str(info["season"]), str(info["episode"])))
		for n in range(len(info["AnimeWorldTitle"])):
			search = "https://www.animeworld.tv/search?keyword={}".format(info["AnimeWorldTitle"][n].replace(" ", "%20"))
			sb_get = requests.get(search, headers = HDR, cookies=cookies)

			if sb_get.status_code == 200:
				soupeddata = BeautifulSoup(sb_get.content, "html.parser")

				page_result = soupeddata.find("div", { "class" : "film-list" }).find_all("a", { "class" : "name" })

				for x in page_result:
					if x.get_text() == info["AnimeWorldTitle"][n]:
						link = "https://www.animeworld.tv" + x.get("href")
						anime_link.append(link)
						break
				else:
					print("L'anime {} non è stato trovato su AnimeWorld.".format(info["AnimeWorldTitle"][n]))
			else:
				print("Accesso negato alla pagina {}.".format(search))
		else:
			if len(anime_link) == 0:
				print(divider, "\n")
				continue

		### Get episode_links ###
		print("Ricerca episode link per {} 𝐒{}𝐄{}.".format(info["SonarrTitle"], str(info["season"]), str(info["episode"])))
		max_eps = 0
		for n in range(len(anime_link)):
			sb_get = requests.get(anime_link[n], headers = HDR, cookies=cookies)
			if sb_get.status_code == 200:
				soupeddata = BeautifulSoup(sb_get.content, "html.parser")


				### providers ###
				providerName = soupeddata.find("span", { "class" : "tabs" }).find_all("span", { "class" : "tab" })
				providers = {}
				for name in providerName:
					providers[name.get_text()] = name["data-name"]
							   # {nome         : id}

				for idProvider in providers.values():
					# print(idProvider)
					epBox = soupeddata.find("div", { "class" : "server", "data-name": str(idProvider)})
					# ep_links = epBox.find_all("a", { "data-toggle" : "tooltip" })
					ep_links = epBox.find_all("a")

					if n < len(anime_link)-1: # nel caso in qui 2 stagioni animeWorld corrispondono ad una di Sonarr
						max_eps += len(ep_links)

					for x in ep_links:
						# print(max_eps, int(x.get_text()), max_eps + int(x.get_text()))
						if (int(x.get_text()) == info["episode"] and n == 0) or ((max_eps + int(x.get_text())) == info["episode"] and n != 0):
							episode_links[idProvider] = "https://www.animeworld.tv" + x.get("href")
							break
			else:
				raise Exception("Accesso negato alla pagina {}.".format(anime_link[n]))
		else:
			if len(episode_links) == 0:
				print("L'episodio {} dell'anime {} non è ancora uscito.".format(str(info["episode"]), info["SonarrTitle"]))
				info = None
				print(divider, "\n")
				continue

		### Get mp4_link ###
		print("Ricerca mp4 link per {} 𝐒{}𝐄{}.".format(info["SonarrTitle"], str(info["season"]), str(info["episode"])))

		if VVVVID in providers and '3' in episode_links: # id = 26
			providerID = providers["VVVVID"]
			episode_link = episode_links[providerID]

			print("\nIl file si trova su {}".format("𝐕𝐕𝐕𝐕𝐈𝐃"))

			anime_id = episode_link.split("/")[-1]
			external_link = "https://www.animeworld.tv/api/episode/serverPlayer?id={}".format(anime_id)

			sb_get = requests.get(episode_link, headers = HDR, cookies=cookies)
			if sb_get.status_code == 200:
				sb_get = requests.get(external_link, headers = HDR, cookies=cookies)
				soupeddata = BeautifulSoup(sb_get.content, "html.parser")
				if sb_get.status_code == 200:
					external = True
					
					raw = soupeddata.find("a", { "class" : "VVVVID-link" })

					mp4_link = raw.get("href")
				else:
					raise Exception(("Accesso negato alla pagina {}.".format(external_link)))
			else:
				raise Exception("Accesso negato alla pagina {}.".format(episode_link))

		elif YouTube in providers and '4' in episode_links: # id = 25
			providerID = providers["YouTube"]
			episode_link = episode_links[providerID]

			print("\nIl file si trova su {}".format("𝐘𝐨𝐮𝐓𝐮𝐛𝐞"))

			anime_id = episode_link.split("/")[-1]
			external_link = "https://www.animeworld.tv/api/episode/serverPlayer?id={}".format(anime_id)

			sb_get = requests.get(episode_link, headers = HDR, cookies=cookies)
			if sb_get.status_code == 200:
				sb_get = requests.get(external_link, headers = HDR, cookies=cookies)
				soupeddata = BeautifulSoup(sb_get.content, "html.parser")
				if sb_get.status_code == 200:
					external = True
					yutubelink_raw = re.findall("https://www.youtube.com/embed/...........", soupeddata.prettify())[0]
					mp4_link = yutubelink_raw.replace("embed/", "watch?v=")

				else:
					raise Exception("Accesso negato alla pagina {}.".format(external_link))
			else:
				raise Exception("Accesso negato alla pagina {}.".format(episode_link))

		elif AnimeWorld_Server in providers and '9' in episode_links: # id = 15
			providerID = providers["AnimeWorld Server"]
			episode_link = episode_links[providerID]

			print("\nIl file si trova su {}".format("𝐀𝐧𝐢𝐦𝐞𝐖𝐨𝐫𝐥𝐝 𝐒𝐞𝐫𝐯𝐞𝐫"))

			anime_id = episode_link.split("/")[-1]
			video_link = "https://www.animeworld.tv/api/episode/serverPlayer?id={}".format(anime_id)
			

			sb_get = requests.get(video_link, headers = HDR, cookies=cookies)
			if sb_get.status_code == 200:
				soupeddata = BeautifulSoup(sb_get.content, "html.parser")

				external = False
				raw_ep = soupeddata.find("video", { "id" : "video-player" }).find("source", { "type" : "video/mp4" })
				mp4_link = raw_ep.get("src")
				# print(mp4_link)
				
			else:
				raise Exception("Accesso negato alla pagina {}.".format(episode_link))

		elif Streamtape in providers and '8' in episode_links: # id = 39 
			providerID = providers["Streamtape"]
			episode_link = episode_links[providerID]

			print("\nIl file si trova su {}".format("𝐒𝐭𝐫𝐞𝐚𝐦𝐭𝐚𝐩𝐞"))

			sb_get = requests.get(episode_link, headers = HDR, cookies=cookies)
			if sb_get.status_code == 200:
				soupeddata = BeautifulSoup(sb_get.content, "html.parser")

				external = False
				site_link = soupeddata.find("div", { "id" : "external-downloads" }).find("a", { "class" : "btn-streamtape" }).get("href")

				sb_get = requests.get(site_link, headers = HDR, cookies=cookies)
				if sb_get.status_code == 200:

					soupeddata = BeautifulSoup(sb_get.content, "html.parser")

					mp4_link = "https://" + re.search(r"document\.getElementById\(\'videolink\'\);elem\[\'innerHTML\'\]=\'\/\/(streamtape\.com\/get_video\?id=.+&expires=.+&ip=.+&token=.+)\';", soupeddata.prettify()).group(1)

				else:
					raise Exception("Accesso negato alla pagina {}.".format(site_link))

			else:
				raise Exception("Accesso negato alla pagina {}.".format(episode_link))


		elif Beta_Server in providers: # id = 10
			print("\nIl file si trova su {}".format("Beta Server"))

			external = False
			print("Il download da {} non è ancora disponibile.".format("𝐁𝐞𝐭𝐚 𝐒𝐞𝐫𝐯𝐞𝐫"))

		else:
			print("Il download da {} non è ancora disponibile.".format("qualche parte"))

		if mp4_link != None:
			info["link"]["url"] = mp4_link
			info["link"]["external"] = external
			seriesNew.append(info)
		else:
			print("Non è stato trovato nessun link per il download dell'episodio {} dell'anime {} (season {})".format(str(info["episode"]), info["SonarrTitle"], str(info["season"])))
		
		print(divider, "\n")
##############
	return seriesNew

def dowload_file(series):
	print("\n◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢𝔻𝕆𝕎𝕃𝕆𝔸𝔻 𝔼ℙ𝕀𝕊𝕆𝔻𝕀◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥◣◥\n")
	print("⏳ Inizio download di {} episodi".format(len(series)))
	serieEdit = []
	for info in series:
		episode = "{nome} - S{season}E{episode}".format(nome=info["SonarrTitle"], season=str(info["season"]), episode=str(info["episode"]))
		episode = episode.replace(":", " ")
		episode = episode.replace("\\", " ")
		episode = episode.replace("/", " ")
		episode = episode.replace("?", " ")
		episode = episode.replace('"', " ")
		episode = episode.replace("<", " ")
		episode = episode.replace(">", " ")
		episode = episode.replace("|", " ")
		episode = episode.replace("*", " ")
		episode = episode.replace("…", " ")
		episode = episode.replace("’", " ")
		info["fileName"] = episode
		serieEdit.append(info)
		print("Episodio {} in download...".format(episode))
		if info["link"]["external"]:
			# youtube-dl
			class MyLogger(object):
				def debug(self, msg):
					pass

				def warning(self, msg):
					pass

				def error(self, msg):
					print(msg)

			def my_hook(d):
				if d['status'] == 'finished':
					print('Dowload Completato.')

			ydl_opts = {
				# 'format': '22/best[height<=720]',
				'outtmpl': episode+'.%(ext)s',
				'logger': MyLogger(),
				'progress_hooks': [my_hook],
			}
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([info["link"]["url"]])
		else:
			# normal download
			r = requests.get(info["link"]["url"], stream = True)
			# download started 
			with open(episode+'.mp4', 'wb') as f:
				total_length = int(r.headers.get('content-length'))
				for chunk in r.iter_content(chunk_size = 1024*1024):
					if chunk: 
						f.write(chunk)
						f.flush()
	else:
		print("✔️ Dowload Completato.")
		return serieEdit

def move_file(series):
	for info in series:
		file = info["fileName"]
		if os.path.isfile(file+'.mp4'):
			file = file + '.mp4'
		elif os.path.isfile(file+'.mkv'):
			file = file + '.mkv'
		else:
			raise

		destinationPath = info["path"]
		currentPath = os.getcwd()
		print("⏳ Spostamento {}.".format(file))

		source = os.path.join(currentPath, file)
		destination = os.path.join(destinationPath, file)
		shutil.move(source, destination)
		print("✔️ File {} spostato.".format(file))

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
		info["AnimeWorldTitle"] = []    # season 1 di sonarr corrisponde a più season di AnimeWorld
		info["season"] = int(serie["seasonNumber"])
		info["episode"] = int(serie["episodeNumber"])
		info["episodeTitle"] = serie["title"]
		info["path"] = os.path.join(ANIME_PATH, serie["series"]["path"].split("/")[-1])
		info["link"] = {}
		info["fileName"] = ""

		series.append(info)

	return series

def RescanSeries(seriesIds):
	print("RescanSeries start...")
	for seriesId in seriesIds:
		endpoint = "command"
		url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
		data = {
			"name": "RescanSeries",
			"seriesId": seriesId
		}
		requests.post(url, json=data)

def RenameSeries(seriesIds):
	print("RenameSeries start...")
	seriesId = 87
	time.sleep(60)
	endpoint = "command"
	url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
	data = {
		"name": "RenameSeries",
		"seriesIds": seriesIds
	}
	requests.post(url, json=data)

#### Telegram ###########################################################################################################

def send_message(series):
	for info in series:
		text = "*Episode Dowloaded*\n{title} - {season}x{episode} - {episodeTitle}".format(title=info["SonarrTitle"], season=str(info["season"]), episode=str(info["episode"]), episodeTitle=info["episodeTitle"])

		url ="https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(BOT_TOKEN, text, CHAT_ID)
		requests.get(url)

if __name__ == '__main__':
	main()
	while True:
		schedule.run_pending()
		time.sleep(1)