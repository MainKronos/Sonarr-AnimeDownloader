from copy import deepcopy
import re
import os
import requests
import animeworld as aw
import json
import shutil
from typing import Dict, List

from utility import Table

from logger import logger
from constants import SETTINGS
import texts as txt
from .exceptions import TableFormattingError

def converting(series:List[Dict]) -> List[Dict]:
	"""
	Con le informazione passate da Sonarr ottiene i rispettivi link di Animeworld.

	```
	return [
	  {
	    "IDs":{
	      "seriesId": int, # ID di Sonarr per la serie
	      "epId": int, # ID di Sonarr per l'episodio
	      "tvdbId": int # ID di TvDB
	    },
	    "SonarrTitle": str, # Titolo della serie di Sonarr
	    "AnimeWorldLinks":[str,...], # Link di AnimeWorld
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


	try:
		res = []

		for anime in series:
			for row in Table.data:
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
				logger.debug(txt.ANIME_INEXISTENT_LOG.format(season=anime["season"], anime=anime["SonarrTitle"]))
				if SETTINGS["AutoBind"]:
					logger.warning(txt.AUTOMATIC_LINK_SEARCH_LOG)
					data = bindAnime(anime["SonarrTitle"], anime["season"], anime["IDs"]["tvdbId"])
					if data is None:
						logger.info(txt.NO_RESULT_LOG)
					else:
						logger.warning(f"{txt.LINK_FOUND_LOG.format(anime=data['name'],link=data['link'])}\n")
						Table.append({
							"title": anime["SonarrTitle"],
							"season": str(anime["season"]),
							"absolute": False,
							"links": [data['link']]
						})

					
	except (json.decoder.JSONDecodeError, KeyError):
		raise TableFormattingError

	return res

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
	ret.sort(key=lambda elem: elem["release"])

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
		logger.warning(txt.FOLDER_CREATION_LOG.format(folder=destinationPath))

	shutil.move(source, destination)
	return True