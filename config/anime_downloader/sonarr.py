from typing import Dict, List
import requests
import time

from logger import logger
from constants import SONARR_URL, API_KEY
import texts as txt

def getMissingEpisodes() -> List[Dict]:
	"""
	Ottiene tutte le informazioni riguardante gli episodi mancanti da Sonarr.

	```
	return [
	  {
	    "IDs":{
	      "seriesId": int, # ID di Sonarr per la serie
	      "epId": int, # ID di Sonarr per l'episodio
	      "tvdbId": int # ID di TvDB
	    },
	    "SonarrTitle": str, # Titolo della serie di Sonarr
	    "AnimeWorldLinks":[], # Link di AnimeWorld (ancora vuoto)
	    "season": int, # Stagione
	    "episode": int, # Episodio
	    "rawEpisode": int, # Episodio Assoluto
	    "episodeTitle": str, # Titolo dell'episodio
	    "path": str # Cartella dell'anime
	  },
	  ...
	]
	```
	"""
	series = []
	endpoint = "wanted/missing"
	page = 0
	error_attempt = 0

	while True:
		try:
			page += 1
			res = requests.get("{}/api/{}?apikey={}&sortKey=airDateUtc&page={}".format(SONARR_URL, endpoint, API_KEY, page))
			result = res.json()

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
					logger.debug(txt.ANIME_REJECTED_LOG.format(anime=serie["series"]["title"], season=serie["seasonNumber"]))
				else:
					series.append(info)
		except requests.exceptions.RequestException as res_error:
			if error_attempt > 3: raise res_error
			error_attempt += 1
			logger.warning(txt.CONNECTION_ERROR_LOG.format(res_error=res_error))
			time.sleep(10)

	return series

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

def getEpisodeFileID(epId): # Converte l'epId in epFileId
	"""
	Trova l'ID del file (`epFileId`) partendo dall'ID dell'episodio (`epId`).

	```
	return int # ID del file
	```
	"""
	data = getEpisode(epId)
	return data["episodeFile"]["id"]