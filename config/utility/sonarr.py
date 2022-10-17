from typing import Dict, List
import requests
import time
import sys

from .tags import Tags

# TODO includere logger a livello globale in modo che sia utilizzabile ovunque(?)
if "utility.logger" not in sys.modules:
	from .logger import logger
from other.constants import SONARR_URL, API_KEY
import other.texts as txt
from other.exceptions import UnauthorizedSonarr

def getMissingEpisodes() -> List[Dict]:
	"""
	Ottiene tutte le informazioni riguardante gli episodi mancanti da Sonarr.

	```
	return [
	  {
	    "title": str, # Titolo della serie di Sonarr
	    "ID": int, # ID di Sonarr per la serie
	    "tvdbID": int, # ID di TvDB
	    "path": str, # Cartella dell'anime
	    "absolute": False, # Se la serie è absolute (a questo livello è sempre False)
	    "seasons": [
	      {
	        "num": str, # Numero stagione
	        "links": [], # Links di AnimeWorld
	        "episodes": [
	          {
	            "num": str, # Numero episodio
	            "abs": str, # Numero assoluto episodio
	            "season": str # Numero stagione
	            "title": str, # Titolo dell'episodio
	            "ID": int # ID di Sonarr per l'episodio
	          },
	          ...
	        ]
	      },
	      ...
	    ]
	  },
	  ...
	]
	```
	"""
	# Prima di cercare gli episodi mancanti aggiorno la lista dei tag con quelli disponibili su Sonarr
	Tags.updateAvailableSonarrTags( getTags() )

	data = []
	endpoint = "wanted/missing"
	page = 0
	error_attempt = 0

	while True:
		try:
			page += 1
			res = requests.get("{}/api/{}?apikey={}&sortKey=airDateUtc&page={}".format(SONARR_URL, endpoint, API_KEY, page))
			result = res.json()

			if "error" in result:
				raise UnauthorizedSonarr(f"Sonarr API KEY non valida, {result['error']}.")

			if len(result["records"]) == 0: 
				break

			for record in result["records"]:

				try:
					if isEligibleSerie( record ) == False: continue # scarta gli episodi che non rispettano i criteri

					def addData():
						while True:
							for anime in data:
								if anime["ID"] == record["seriesId"]:
									for season in anime["seasons"]:
										if season["num"] == str(record["seasonNumber"]):

											season["episodes"].append({
												"num": str(record["episodeNumber"]),
												"abs": str(record["absoluteEpisodeNumber"]) if "absoluteEpisodeNumber" in record else None,
												"season": str(record["seasonNumber"]),
												"title": record["title"],
												"ID": record["id"]
											})
											return
									else:
										anime["seasons"].append({
											"num": str(record["seasonNumber"]),
											"links": [],
											"episodes": []
										})
										break
							else:
								data.append({
									"title": record["series"]["title"],
									"ID": record["seriesId"],
									"tvdbID": record["series"]["tvdbId"],
									"path": record["series"]["path"],
									"absolute": False,
									"seasons": []
								})
					addData()
				except KeyError:
					data.pop()
					logger.debug(txt.ANIME_REJECTED_LOG.format(anime=record["series"]["title"], season=record["seasonNumber"]) + '\n')
		except requests.exceptions.RequestException as res_error:
			if error_attempt > 3: raise res_error
			error_attempt += 1
			logger.warning(txt.CONNECTION_ERROR_LOG.format(res_error=res_error) + '\n')
			time.sleep(10)

	return data

def rescanSerie(seriesId:int):
	"""
	Esegue un rescan della serie `seriesId`.
	"""
	endpoint = "command"
	url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
	data = {
		"name": "RescanSeries",
		"seriesId": seriesId
	}
	requests.post(url, json=data)

def renameSerie(seriesId:int):
	"""
	Rinomina tutti gli episodio che non seguono la formattazione di Sonarr per la serie `seriesId`.
	"""
	endpoint = "command"
	url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
	data = {
		"name": "RenameSeries",
		"seriesIds": [seriesId]
	}
	requests.post(url, json=data)

def getEpisode(epId:int) -> Dict:
	"""
	Ottiene tutte le informazioni da Sonarr riguardante l'episodio `epId`.
	"""
	endpoint = f"episode/{epId}"
	url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
	return requests.get(url).json()

def renameEpisode(seriesId:int, epFileId:int):
	"""
	Rinomina lil file `epFileId` della serie `seriesId` seguendo la formattazione di Sonarr.
	"""
	endpoint = "command"
	url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
	data = {
		"name": "RenameFiles",
		"seriesId": seriesId,
		"files": [epFileId]
	}
	requests.post(url, json=data)

def getEpisodeFileID(epId:int) -> int: # Converte l'epId in epFileId
	"""
	Trova l'ID del file (`epFileId`) partendo dall'ID dell'episodio (`epId`).

	```
	return int # ID del file
	```
	"""
	data = getEpisode(epId)
	return data["episodeFile"]["id"]
	
def inQueue(epId:int) -> bool:
	"""
	Controlla se l'episodio è in download da Sonarr.
	"""
	endpoint = "queue"
	url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
	return epId in [x["episode"]["id"] for x in requests.get(url).json()]

def getSerieInfo(serieId:int):
	"""
	Recupera le informazioni per una serie specifica
	"""
	endpoint = f"series/{serieId}"
	url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
	return requests.get(url).json()

def getTags():
	"""
	Recupera la lista dei tag presenti su sonarr
	"""
	try:
		endpoint = "tag"
		url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
		return requests.get(url).json()
	
	except Exception:
		return []

def isEligibleSerie( record ) -> bool:
	"""
	Verifica se la serie restituita da Sonarr è idonea ad essere scaricata secondo le attuali impostazioni ( tag e tipologia serie anime )
	"""
	# Comportamento standard: la serie deve avere come tipologia ANIME su Sonarr
	if record["series"]["seriesType"] != 'anime': return False

	res = True

	activeTags = [x for x in Tags.data if x["active"] == True] 

	def tagInclusiveExists():
		for tag in activeTags:
			if tag["inclusive"] == True:
				return True
		else:
			return False

	# Se esistono dei tag li controllo
	if len(activeTags):
		# Se esiste un tag inclusivo tra i miei l'azione di default deve essere di escludere tutti gli anime e accettare solo quelli con tag inclusivo
		res = tagInclusiveExists()

		serieId = record["seriesId"]
		serie = getSerieInfo( serieId )	

		# Ordino prima quelli inclusivi, poi esclusivi
		activeTags.sort(key=lambda x: x["inclusive"], reverse=True)

		for tag in activeTags:
			if tag["id"] in serie["tags"]:
				res = tag["inclusive"] == True

	return res
