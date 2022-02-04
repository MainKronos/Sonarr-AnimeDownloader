#!/usr/bin/python3

import animeworld as aw
import requests
import os, re, json
from copy import deepcopy
import schedule
import time
import threading
import shutil
import logging.config; logger = logging.getLogger(__name__)
from app import app, ReadSettings, appendAnime

SETTINGS = ReadSettings()

DOWNLOAD_FOLDER = '/downloads'

SONARR_URL = os.getenv('SONARR_URL') # Indirizzo ip + porta di sonarr
API_KEY = os.getenv('API_KEY') # Chiave api di sonarr
CHAT_ID = os.getenv('CHAT_ID') # telegramm
BOT_TOKEN = os.getenv('BOT_TOKEN') # telegramm

SCHEDULE_MINUTES = SETTINGS["ScanDalay"] # Ripetizione

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
	LoadLog()
	logger.warning(start)

	if SONARR_URL is None:
		logger.warning("✖️ Variabile d'ambinete '𝙎𝙊𝙉𝘼𝙍𝙍_𝙐𝙍𝙇' non inserita.")
	else:
		logger.info("✔ 𝙎𝙊𝙉𝘼𝙍𝙍_𝙐𝙍𝙇: {}".format(SONARR_URL))
	if API_KEY is None:
		logger.warning("✖️ Variabile d'ambinete '𝘼𝙋𝙄_𝙆𝙀𝙔' non inserita.")
	else:
		logger.info("✔ 𝘼𝙋𝙄_𝙆𝙀𝙔: {}".format(API_KEY))
	if CHAT_ID is None:
		logger.debug("✖️ Variabile d'ambinete '𝘾𝙃𝘼𝙏_𝙄𝘿' non inserita.")
	else:
		logger.info("✔ 𝘾𝙃𝘼𝙏_𝙄𝘿: {}".format(CHAT_ID))
	if BOT_TOKEN is None:
		logger.debug("✖️ Variabile d'ambinete '𝘽𝙊𝙏_𝙏𝙊𝙆𝙀𝙉' non inserita.")
	else:
		logger.info("✔ 𝘽𝙊𝙏_𝙏𝙊𝙆𝙀𝙉: {}".format(BOT_TOKEN))

	if None not in (SONARR_URL, API_KEY):
		logger.info(f"\n{OKC}☑️ Le variabili d'ambiente sono state inserite correttamente.{NC}\n")

		logger.info(f"\n⚙️ Intervallo Scan: {SCHEDULE_MINUTES} minuti\n")

		logger.info("\nAVVIO SERVER")
		job_thread = threading.Thread(target=server)
		job_thread.start()

		job() # Fa una prima esecuzione e poi lo imposta per la ripetizione periodica
		schedule.every(SCHEDULE_MINUTES).minutes.do(job)


def server():
	app.run(debug=False, host='0.0.0.0', use_reloader=False)


def run_threaded(job_func):
	job_thread = threading.Thread(target=job_func)
	job_thread.start()

def job():
	divider = f"{DIVIDC}- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - {NC}"
	
	logger.warning("\n{color}╭-----------------------------------「{time}」-----------------------------------╮{nc}\n".format(time=time.strftime("%d %b %Y %H:%M:%S"), color=SEPARC, nc=NC))

	try:
		raw_series = get_missing_episodes()
		if len(raw_series)!=0:
			series = converting(raw_series)

			for info in series:
				logger.warning(f"\n{divider}")

				try:
					logger.warning("🔎 Ricerca anime '{}' per l'episodio S{}E{}.".format(info["SonarrTitle"], info["season"], info["rawEpisode"]))
					anime = [aw.Anime(link=x) for x in info["AnimeWorldLinks"]]

					logger.info("🔎 Ricerca degli episodi per '{}'.".format(info["SonarrTitle"]))
					epsArr = [x.getEpisodes() for x in anime] # array di episodi da accorpare
					episodi = fixEps(epsArr)

					logger.info("⚙️ Verifica se l'episodio 𝐒{}𝐄{} è disponibile.".format(info["season"], info["rawEpisode"]))
					ep = None
					for episodio in episodi:
						if episodio.number == str(info["episode"]):
							ep = episodio
							logger.info("✔️ L'episodio è disponibile.")
							break
					else:
						logger.info("✖️ L'episodio NON è ancora uscito.")

					if ep is not None: # Se l'episodio è disponibile
						logger.warning("⏳ Download episodio 𝐒{}𝐄{}.".format(info["season"], info["rawEpisode"]))
						title = f'{info["SonarrTitle"]} - S{info["season"]}E{info["rawEpisode"]}'
						if ep.number == str(info["episode"]):
							fileLink = ep.links[0]
							if fileLink.download(title, DOWNLOAD_FOLDER): 
								logger.info("✔️ Dowload Completato.")

						if SETTINGS["MoveEp"]:
							logger.info("⏳ Spostamento episodio 𝐒{}𝐄{} in {}.".format(info["season"], info["rawEpisode"], info["path"]))
							if move_file(os.path.join(DOWNLOAD_FOLDER,title), info["path"]): 
								logger.info("✔️ Episodio spostato.")

							logger.info("⏳ Ricaricando la serie '{}'.".format(info["SonarrTitle"]))
							RescanSerie(info["IDs"]["seriesId"])

							if SETTINGS["RenameEp"]:
								logger.info("⏳ Rinominando l'episodio.")
								for i in range(5): # Fa 5 tentativi
									try:
										time.sleep(1)
										epFileId = GetEpisodeFileID(info["IDs"]["epId"])
									except KeyError:
										continue
									else:
										RenameEpisode(info["IDs"]["seriesId"], epFileId)
										break
								else:
									logger.warning(f"⚠️ NON è stato possibile rinominare l'episodio.")

							if None not in (CHAT_ID, BOT_TOKEN):
								logger.info("✉️ Inviando il messaggio via telegram.")
								send_message(info)

				except requests.exceptions.RequestException as res_error:
					logger.warning(f"⚠️ Errore di connessione. ({res_error})")
				except aw.AnimeNotAvailable as info:
					logger.warning(f"⚠️ {info}")
				except aw.ServerNotSupported as warning:
					logger.error(f"{WARNC}🆆🅰🆁🅽🅸🅽🅶: {warning}{NC}")
				except aw.DeprecatedLibrary as dev:
					logger.critical(f"{ALERTC}🅰🅻🅴🆁🆃: {dev}{NC}")
				finally:
					logger.warning(f"\n{divider}")

		else:
			logger.info("\nNon c'è nessun episodio da cercare.\n")

	except requests.exceptions.RequestException as res_error:
		logger.error(f"🆆🅰🆁🅽🅸🅽🅶: Errore di connessione. ({res_error})")	
	except Exception as error:
		logger.exception(f"{ERRORC}🅴🆁🆁🅾🆁: {error}{NC}")

	nextStart = time.strftime("%d %b %Y %H:%M:%S", time.localtime(time.time() + SCHEDULE_MINUTES*60))
	logger.warning("\n{color}╰-----------------------------------「{time}」-----------------------------------╯{nc}\n".format(time=nextStart, color=SEPARC, nc=NC))

def fixEps(epsArr): # accorpa 2 o più serie di animeworld
	up = 0 # numero da aggiungere per rendere consecutivi gli episodi di varie stagioni
	ret = []

	for eps in epsArr:
		for ep in eps:
			if re.search(r'^\d+$', ep.number) is not None: # Episodio intero
				ep.number = str(int(ep.number) + up)
				ret.append(ep)

			if re.search(r'^\d+\.\d+$', ep.number) is not None: # Episodio fratto
				continue # lo salta perchè sicuramente uno speciale

			if re.search(r'^\d+-\d+$', ep.number) is not None: # Episodio Doppio
				ep1 = deepcopy(ep)   # Duplica l'episodio da sitemare la gestione.....
				ep2 = deepcopy(ep)   # Non mi piace


				ep1.number = str(int(ep.number.split('-')[0]) + up)
				ep2.number = str(int(ep.number.split('-')[1]) + up)

				ret.extend([ep1, ep2])
			
		up += int(eps[-1].number)

	return ret

def bindAnime(anime_name:str, season:int, thetvdb_id:int) -> dict:

	# ottengo tutti gli ids
	db = requests.get("https://raw.githubusercontent.com/Fribb/anime-lists/master/anime-list-full.json").json()

	# filtro tutti gli ids alla ricerca di tutti i dizionari che contengono lo stesso id di thetvdb
	ids = [
		{
			"thetvdb_id": elem["thetvdb_id"], 
			"mal_id": elem["mal_id"]
		} 
		for elem in db if "thetvdb_id" in elem and elem["thetvdb_id"] == thetvdb_id and elem["type"] == "TV"
	]

	# ottengo tutti i risultati da animewolrd ricercando solamente con il nome dell'anime
	results = aw.find(anime_name)

	ret = []

	for res in results:
		# controlla se è doppiato, e se lo fosse lo scarta
		if res["dub"]: continue

		# controllo se l'id di MAL è presente tra tutti gli id che ho filtrato precedentemente
		if len([x for x in ids if x["mal_id"] == res["malId"]]) != 0:
			ret.append({
				"name": res["name"],
				"release": res["release"],
				"link": res["link"]
			})

	# riordino per data di uscita
	ret.sort(key=lambda elem: elem["release"])

	# controllo se effettivamente esiste la stagione
	if len(ret) < season: return None
	else:
		# ritorno nome e link
		return {
			"name": ret[season-1]["name"],
			"link": ret[season-1]["link"]
		}


def converting(series):
	json_location = "/script/json/table.json"

	if not os.path.exists(json_location):
		logger.warning("⚠️ Il file table.json non esiste, quindi verrà creato.")
		with open(json_location, 'w') as f:
			f.write("[]")

	try:
		f = open(json_location, 'r')
		table = json.loads(f.read())
		f.close()

		res = []

		for anime in series:
			for row in table:
				if row["title"] == anime["SonarrTitle"]:
					if row["absolute"]:
						tmp = int(anime["episode"])
						anime["episode"] = int(anime["rawEpisode"])
						anime["rawEpisode"] = tmp

						anime["AnimeWorldLinks"] = list(row["seasons"]["absolute"])
						res.append(anime)
						break
					elif str(anime["season"]) in row["seasons"].keys():
						anime["rawEpisode"] = int(anime["episode"])

						anime["AnimeWorldLinks"] = list(row["seasons"][str(anime["season"])])
						res.append(anime)
						break
			else:
				logger.debug("❌ La 𝘴𝘵𝘢𝘨𝘪𝘰𝘯𝘦 {} della 𝘴𝘦𝘳𝘪𝘦 '{}' non esiste nella 𝗧𝗮𝗯𝗲𝗹𝗹𝗮 𝗗𝗶 𝗖𝗼𝗻𝘃𝗲𝗿𝘀𝗶𝗼𝗻𝗲.".format(anime["season"], anime["SonarrTitle"]))
				if SETTINGS["AutoBind"]:
					logger.warning("⚠️ Ricerca automatica link di AnimeWorld.")
					data = bindAnime(anime["SonarrTitle"], anime["season"], anime["IDs"]["tvdbId"])
					if data is None:
						logger.info("⛔ Nessun risultato trovato.")
					else:
						logger.warning(f"✳️ Risultato trovato, verrà utilizzato nella prossima ricerca: \n- {data['name']} ({data['link']}).\n")
						appendAnime({
							"title": anime["SonarrTitle"],
							"season": str(anime["season"]),
							"absolute": False,
							"links": [data['link']]
						})

					
	except (json.decoder.JSONDecodeError, KeyError):
		raise TableFormattingError

	return res

def move_file(source, destinationPath):
	
	
	if os.path.isfile(source+'.mp4'):
		source = source + '.mp4'
	elif os.path.isfile(source+'.mkv'):
		source = source + '.mkv'
	else:
		return False
	
	file = source.split(os.path.sep)[-1]

	destinationPath = destinationPath.replace('\\', '/')
	destinationPath = re.sub(r"\w:", "", destinationPath)

	destination = os.path.join(destinationPath, file)

	if not os.path.exists(destinationPath):
		os.makedirs(destinationPath)
		logger.warning(f"⚠️ La cartella {destinationPath} è stata creata.")

	shutil.move(source, destination)
	return True

#### Sonarr ############################################################################################################

def get_missing_episodes():
	series = []
	endpoint = "wanted/missing"
	page = 0
	error_attempt = 0

	while True:
		try:
			page += 1
			res = requests.get("{}/api/{}?apikey={}&sortKey=airDateUtc&page={}".format(SONARR_URL, endpoint, API_KEY, page))
			result = res.json()

			# f = open("res.json", 'w')
			# f.write(json.dumps(result, indent=4))
			# f.close()

			if len(result["records"]) == 0: 
				break

			for serie in result["records"]:

				try:
					if serie["series"]["seriesType"] != 'anime': continue
					info = {}
					info["IDs"] = {
						"seriesId": serie["seriesId"],
						"epId": serie["id"],
						"tvdbId": serie["series"]["tvdbId"]
					}
					info["SonarrTitle"] = serie["series"]["title"]
					info["AnimeWorldLinks"] = []    # season 1 di sonarr corrisponde a più season di AnimeWorld
					info["season"] = int(serie["seasonNumber"])
					info["episode"] = int(serie["episodeNumber"])
					info["rawEpisode"] = int(serie["absoluteEpisodeNumber"])
					info["episodeTitle"] = serie["title"]
					info["path"] = serie["series"]["path"]
				except KeyError:
					logger.debug("⁉️ Serie '{}' S{} scartata per mancanza di informazioni.".format(serie["series"]["title"], serie["seasonNumber"]))
				else:
					series.append(info)
		except requests.exceptions.RequestException as res_error:
			if error_attempt > 3: raise res_error
			error_attempt += 1
			logger.warning(f"⚠️ Errore di connessione, prossimo tentativo fra 10s. ({res_error})")
			time.sleep(10)

	return series

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
		"seriesIds": [seriesId]
	}
	requests.post(url, json=data)

def GetEpisode(epId):
	endpoint = f"episode/{epId}"
	url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
	return requests.get(url)

def GetEpisodeFile(epFileId):
	endpoint = f"episodefile/{epFileId}"
	url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
	return requests.get(url)

def RenameEpisode(seriesId, epFileId):
	endpoint = "command"
	url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
	data = {
		"name": "RenameFiles",
		"seriesId": seriesId,
		"files": [epFileId]
	}
	return requests.post(url, json=data)

### UTILS

def GetEpisodeFileID(epId): # Converte l'epId in epFileId
	data = GetEpisode(epId).json()
	return data["episodeFile"]["id"]

### LOG

def LoadLog():

	logging.basicConfig(format='%(message)s')
	# 

	# sh = logging.StreamHandler()
	# sh.setFormatter(logging.Formatter('%(message)s'))
	# logger.addHandler(sh)

	fh = logging.FileHandler('log.log', encoding='utf-8')
	fh.setFormatter(logging.Formatter("%(message)s"))
	logger.addHandler(fh)

	logging.getLogger("urllib3").setLevel(logging.WARNING)
	logging.getLogger("requests").setLevel(logging.WARNING)

	

	
	SetLog()

def SetLog():
	LogLevel = SETTINGS["LogLevel"]
	logging.getLogger().setLevel(LogLevel)


#### Telegram ###########################################################################################################

def send_message(info):
	text = "*Episode Downloaded*\n{title} - {season}x{episode} - {episodeTitle}".format(title=info["SonarrTitle"], season=str(info["season"]), episode=str(info["episode"]), episodeTitle=info["episodeTitle"])

	url ="https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(BOT_TOKEN, text, CHAT_ID)
	requests.get(url)

if __name__ == '__main__':
	main()
	while True:
		schedule.run_pending()
		time.sleep(1)

### FLASK #######################


### ERRORI ####################################

# Problema alla formattazione del file table.json
class TableFormattingError(Exception):
	def __init__(self):
		self.message = "Errore al file table.json"
		super().__init__(self.message)
