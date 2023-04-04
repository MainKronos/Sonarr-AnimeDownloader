from copy import deepcopy
import re
import os
import requests
import animeworld as aw
import json
import shutil
from datetime import datetime
from typing import Dict, List
import time


from app import socketio

from .table import Table
from .logger import logger, message
from .settings import Settings
from . import sonarr
import other.texts as txt
from other.exceptions import TableFormattingError

def converting(data:List[Dict]) -> List[Dict]:
	"""
	Con le informazione passate da Sonarr ottiene i rispettivi link di Animeworld.

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
	        "links": [str,...], # Links di AnimeWorld
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

	def linkSearch(title: str, season: str, tvdbID:int) -> str:
		"""
		Cerca i link di animeworld e notifica l'utente.
		"""
		logger.warning(txt.AUTOMATIC_LINK_SEARCH_LOG.format(season=season, anime=title) + '\n')
		result = bindAnime(title, int(season), tvdbID)
		if result is None:
			logger.info(txt.NO_RESULT_LOG + '\n')
		else:
			logger.warning(txt.LINK_FOUND_LOG.format(anime=result['name'],link=result['link']) + '\n\n')
			message.warning(txt.CONNECTION_LINK_FOUND_LOG.format(sanime=title, sseason=season, anime=result['name'],link=result['link']))
			Table.append({
				"title": title,
				"season": str(season),
				"absolute": False,
				"links": [result['link']]
			})
			return result['link']
		
	

	try:
		for anime in data:
			for row in Table.data:
				if row["title"] == anime["title"]:
					if row["absolute"]: # se la serie ha un ordinamento assoluto
						if "absolute" in row["seasons"]: # se esiste la stagione "absolute"
							anime["absolute"] = True
							season_absolute = {
								"num": "absolute",
								"links": list(row["seasons"]["absolute"]), # aggiunge i link di AnimeWorld
								"episodes": []
							}
							while True:
								try:
									season = anime["seasons"].pop(0) # rimuove ogni stagione
								except IndexError: # finche esistono
									break				
								else:
									for episode in season["episodes"]: # controlla che ogni episodio della stagione abbia la numerazione assoluta
										if episode["abs"]:
											season_absolute["episodes"].append(episode) # aggiunge ogni episodio nella stagione ABSOLUTE
										else:
											logger.debug(txt.EPISODE_REJECTED_LOG.format(anime=anime["title"], season=season["num"], episode=episode["num"]) + '\n')

							if len(season_absolute["episodes"]) != 0:
								anime["seasons"].append(season_absolute)
							break
						else:
							# La serie risulta con ordinamento assoluto ma non esiste la stagione "absolute" nella tabella
							logger.debug(txt.SEASON_INEXISTENT_LOG.format(season=", ".join([x["num"] for x in anime["seasons"]]), anime=anime["title"]) + '\n')

							if Settings.data["AutoBind"]: # ricerca automatica links
								logger.debug(txt.ABSOLUTE_AUTOMATIC_LINK_SEARCH_ERROR_LOG + '\n')

							break
	
					else:
						for season in anime["seasons"]:
							if season["num"] not in row["seasons"] or len(list(row["seasons"][season["num"]])) == 0:
								if season["num"] != '0':
									# La stagione non esiste nella tabella
									if season["num"] not in row["seasons"]: 
										logger.debug(txt.SEASON_INEXISTENT_LOG.format(season=season["num"], anime=anime["title"]) + '\n')

									# il link non esiste nella tabella
									elif len(list(row["seasons"][season["num"]])):
										logger.debug(txt.LINK_INEXISTENT_LOG.format(season=season["num"], anime=anime["title"]) + '\n')

									if Settings.data["AutoBind"]: # ricerca automatica links
										link = linkSearch(anime["title"], season["num"], anime["tvdbID"])
										if link is not None: season["links"] = [link]
								else:
									logger.debug(txt.SPECIAL_AUTOMATIC_LINK_SEARCH_ERROR_LOG + '\n')
							else:
								season["links"] = list(row["seasons"][season["num"]]) # aggiunge i link di AnimeWorld
							
								

						break
			else:
				# L'anime non esiste nella tabella
				logger.debug(txt.ANIME_INEXISTENT_LOG.format(anime=anime["title"]) + '\n')

				if Settings.data["AutoBind"]: # ricerca automatica links
					for season in anime["seasons"]:
						if season["num"] != '0':
							link = linkSearch(anime["title"], season["num"], anime["tvdbID"])
							if link is not None: season["links"] = [link]
						else:
							logger.debug(txt.SPECIAL_AUTOMATIC_LINK_SEARCH_ERROR_LOG + '\n')

			

			# rimuove le stagioni senza links
			anime["seasons"] = list(filter(lambda season: len(season["links"]) != 0, anime["seasons"]))

					
	except (json.decoder.JSONDecodeError, KeyError):
		raise TableFormattingError

	return list(filter(lambda anime: len(anime["seasons"]) != 0, data)) # rimuove gli anime senza stagioni

def fixEps(epsArr:List[List[aw.Episodio]]) -> List[aw.Episodio]:
	"""
	Accorpa 2 o più serie di animeworld.

	```
	return [
	  Episodio, # Classe Episodio
	  ..
	]
	```
	"""
	up = 0 # numero da aggiungere per rendere consecutivi gli episodi di varie stagioni
	ret = []

	for eps in epsArr:
		for ep in eps:
			if re.search(r'^\d+$', ep.number) is not None: # Episodio intero
				ep.number = str(int(ep.number) + up)
				ret.append(ep)

			elif re.search(r'^\d+\.\d+$', ep.number) is not None: # Episodio fratto
				continue # lo salta perchè sicuramente uno speciale

			elif re.search(r'^\d+-\d+$', ep.number) is not None: # Episodio Doppio
				ep1 = deepcopy(ep)   # Duplica l'episodio da sitemare la gestione.....
				ep2 = deepcopy(ep)   # Non mi piace


				ep1.number = str(int(ep.number.split('-')[0]) + up)
				ep2.number = str(int(ep.number.split('-')[1]) + up)

				ret.extend([ep1, ep2])
			
		up = int(eps[-1].number)

	return ret

def bindAnime(anime_name:str, season:int, thetvdb_id:int) -> Dict[str,str]:
	"""
	Restituisce il link e e il nome dell'anime trovato su AnimeWolrd.

	```
	return {
	  "name": str, # Nome dell'anime
	  "link": str # Link dell'anime
	}
	```
	"""
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
	ret.sort(key=lambda elem: (elem["release"] is None, elem["release"]))

	# controllo se effettivamente esiste la stagione
	if len(ret) < season: return None
	else:
		# ritorno nome e link
		return {
			"name": ret[season-1]["name"],
			"link": ret[season-1]["link"]
		}

def movefile(source, destinationPath):
	"""
	Sposta un file da una cartella in un'altra.
	"""
	
	file = source.split(os.path.sep)[-1]

	destinationPath = destinationPath.replace('\\', '/')
	destinationPath = re.sub(r"\w:", "", destinationPath)

	destination = os.path.join(destinationPath, file)

	if not os.path.exists(destinationPath):
		os.makedirs(destinationPath)
		logger.warning(txt.FOLDER_CREATION_LOG.format(folder=destinationPath) + '\n')

	shutil.move(source, destination)
	return True

def getLatestVersion():
	try:
		return requests.get("https://api.github.com/repos/MainKronos/Sonarr-AnimeDownloader/releases").json()[0]["name"]
	except Exception:
		return

def downloadProgress(d):
	"""
	Stampa il progresso di download dell'episodio.
	"""
	
	if int(datetime.timestamp(datetime.now()) - downloadProgress.step ) > 0 or d["percentage"] == 1:
		socketio.emit("download_info", d)
		downloadProgress.step = datetime.timestamp(datetime.now())

downloadProgress.step = datetime.timestamp(datetime.now())

def downloadControl(args: Dict[str,str], opt: List[str]):
	"""
	Controlla il download del file.
	`opt`: opzioni da modificare.
	`args`: {
		active: bool
		epId: int
	}
	"""

	while args["active"]:
		if sonarr.inQueue(args["epId"]):
			opt.append('abort')
			return
		time.sleep(60)
