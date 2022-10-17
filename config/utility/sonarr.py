from typing import Dict, List
import requests
import time

from .logger import logger
from other.constants import SONARR_URL, API_KEY
import other.texts as txt
from other.exceptions import UnauthorizedSonarr

# https://sonarr.tv/docs/api/
# https://github.com/Sonarr/Sonarr/wiki/API (Legacy)

class Sonarr:

	def __ApiRequest(fun):
		"""
		Funzione che controlla che l'url e l'API-key siano validi e fa 3 tentativi di richiesta, se falliscono solleva un errore.
		"""
		def wrapper(self, *args, **kwargs):
			error_attempt = 0
			while True:
				try:
					result = fun(self, *args, **kwargs)

					if "error" in result:
						raise UnauthorizedSonarr(f"Sonarr API KEY non valida, {result['error']}.")
					
					return result
				except requests.exceptions.RequestException as e:
					if error_attempt > 3: raise e
					error_attempt += 1
					logger.warning(txt.CONNECTION_ERROR_LOG.format(res_error=e) + '\n')
					time.sleep(10)
		return wrapper
	
	@__ApiRequest
	def __getApiRequest(self, url:str):
		res = requests.get(url)
		return res.json()
	
	@__ApiRequest
	def __postApiRequests(self, url:str, data:Dict):
		res = requests.get(url, json=data)
		return res.json()

	def getMissingEpisodes(self) -> List[Dict]:
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
		data = []
		endpoint = "wanted/missing"
		page = 0

		while True:
			page += 1
			result = self.__getApiRequest("{}/api/{}?apikey={}&sortKey=airDateUtc&page={}".format(SONARR_URL, endpoint, API_KEY, page))

			if len(result["records"]) == 0: 
				break

			for record in result["records"]:

				try:
					if record["series"]["seriesType"] != 'anime': continue # scarta gli episodi che non sono anime

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

		return data

	def rescanSerie(self, seriesId:int):
		"""
		Esegue un rescan della serie `seriesId`.
		"""
		endpoint = "command"
		url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
		data = {
			"name": "RescanSeries",
			"seriesId": seriesId
		}
		self.__postApiRequests(url, json=data)

	def renameSerie(self, seriesId:int):
		"""
		Rinomina tutti gli episodio che non seguono la formattazione di Sonarr per la serie `seriesId`.
		"""
		endpoint = "command"
		url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
		data = {
			"name": "RenameSeries",
			"seriesIds": [seriesId]
		}
		self.__postApiRequests(url, json=data)

	def getEpisode(self, epId:int) -> Dict:
		"""
		Ottiene tutte le informazioni da Sonarr riguardante l'episodio `epId`.
		"""
		endpoint = f"episode/{epId}"
		url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
		return self.__getApiRequest(url)

	def renameEpisode(self, seriesId:int, epFileId:int):
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
		self.__postApiRequests(url, json=data)

	def getEpisodeFileID(self, epId:int) -> int: # Converte l'epId in epFileId
		"""
		Trova l'ID del file (`epFileId`) partendo dall'ID dell'episodio (`epId`).

		```
		return int # ID del file
		```
		"""
		data = self.getEpisode(epId)
		return data["episodeFile"]["id"]

	def inQueue(self, epId:int) -> bool:
		"""
		Controlla se l'episodio è in download da Sonarr.
		"""
		endpoint = "queue"
		url = "{}/api/{}?apikey={}".format(SONARR_URL, endpoint, API_KEY)
		return epId in [x["episode"]["id"] for x in self.__getApiRequest(url)]