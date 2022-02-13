import time

import requests
import animeworld as aw
import os

import texts as txt
from logger import logger
from constants import CHAT_ID, BOT_TOKEN, SETTINGS, DOWNLOAD_FOLDER

from .functions import converting, fixEps, movefile
from . import sonarr
from . import telegram

def job():
	"""
	Esegue la ricerca degli episodi mancanti, se li trova li scarica.
	"""
	logger.warning(f"\n{txt.START_BLOCK_LOG.format(time=time.strftime('%d %b %Y %H:%M:%S'))}\n")

	try:
		raw_series = sonarr.getMissingEpisodes()
		if len(raw_series)!=0:
			series = converting(raw_series)

			for info in series:
				logger.warning(f"\n{txt.DIVIDER_LOG}")

				try:
					logger.warning(txt.ANIME_RESEARCH_LOG.format(anime=info["SonarrTitle"], season=info["season"], episode=info["rawEpisode"]))
					anime = [aw.Anime(link=x) for x in info["AnimeWorldLinks"]]

					logger.info(txt.EPISODE_RESEARCH_LOG.format(anime=info["SonarrTitle"]))
					epsArr = [x.getEpisodes() for x in anime] # array di episodi da accorpare
					episodi = fixEps(epsArr)

					logger.info(txt.CHECK_EPISODE_AVAILABILITY_LOG.format(season=info["season"], episode=info["rawEpisode"]))
					ep = None
					for episodio in episodi:
						if episodio.number == str(info["episode"]):
							ep = episodio
							logger.info(txt.EPISODE_AVAILABLE_LOG)
							break
					else:
						logger.info(txt.EPISODE_UNAVAILABLE_LOG)

					if ep is not None: # Se l'episodio è disponibile
						logger.warning(txt.EPISODE_DOWNLOAD_LOG.format(season=info["season"], episode=info["rawEpisode"]))
						title = f'{info["SonarrTitle"]} - S{info["season"]}E{info["rawEpisode"]}'
						if ep.number == str(info["episode"]):
							fileLink = ep.links[0]

							file = ep.download(title, DOWNLOAD_FOLDER)
							if file: 
								logger.info(txt.DOWNLOAD_COMPLETED_LOG)

						if SETTINGS["MoveEp"]:
							logger.info(txt.EPISODE_SHIFT_LOG.format(season=info["season"], episode=info["rawEpisode"], folder=info["path"]))
							if movefile(os.path.join(DOWNLOAD_FOLDER,file), info["path"]): 
								logger.info(txt.EPISODE_SHIFT_DONE_LOG)

							logger.info(txt.ANIME_REFRESH_LOG.format(anime=info["SonarrTitle"]))
							sonarr.rescanSerie(info["IDs"]["seriesId"])

							if SETTINGS["RenameEp"]:
								logger.info(txt.EPISODE_RENAME_LOG)
								for i in range(5): # Fa 5 tentativi
									try:
										time.sleep(1)
										epFileId = sonarr.getEpisodeFileID(info["IDs"]["epId"])
									except KeyError:
										continue
									else:
										sonarr.renameEpisode(info["IDs"]["seriesId"], epFileId)
										break
								else:
									logger.warning(txt.EPISODE_RENAME_ERROR_LOG)

							if None not in (CHAT_ID, BOT_TOKEN):
								logger.info(txt.SEND_TELEGRAM_MESSAGE_LOG)
								telegram.sendMessage(info)

				except requests.exceptions.RequestException as res_error:
					logger.warning(txt.CONNECTION_ERROR_LOG.format(res_error=res_error))
				except aw.AnimeNotAvailable as info:
					logger.warning(txt.WARNING_STATE_LOG.format(warning=info))
				except aw.ServerNotSupported as warning:
					logger.error(txt.ERROR_STATE_LOG.format(error=warning))
				except aw.DeprecatedLibrary as dev:
					logger.critical(txt.CRITICAL_STATE_LOG.format(critical=dev))
				finally:
					logger.warning(f"\n{txt.DIVIDER_LOG}")

		else:
			logger.info(f"\n{txt.NO_EPISODES}\n")

	except requests.exceptions.RequestException as res_error:
		logger.error(txt.CONNECTION_ERROR_LOG.format(res_error=res_error))	
	except Exception as error:
		logger.exception(txt.EXCEPTION_STATE_LOG.format(exception=error))

	nextStart = time.strftime("%d %b %Y %H:%M:%S", time.localtime(time.time() + SETTINGS["ScanDelay"]*60))
	logger.warning(f"\n{txt.END_BLOCK_LOG.format(time=nextStart)}\n")


