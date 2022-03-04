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

			for anime in series:
				for season in anime["seasons"]:
					logger.warning(f"\n{txt.DIVIDER_LOG}\n")
					try:
						logger.warning(txt.ANIME_RESEARCH_LOG.format(anime=anime["title"], season=season["num"]))

						results = [aw.Anime(link=x) for x in season["links"]]

						logger.info(txt.EPISODE_RESEARCH_LOG.format(episode=", ".join([x["num"] for x in season["episodes"]])))

						episodi = fixEps([x.getEpisodes() for x in results])

						for episode in season["episodes"]:
							logger.info(f'\n{txt.CHECK_EPISODE_AVAILABILITY_LOG.format(season=episode["season"], episode=episode["num"])}')
							for ep in episodi:
								
								# episodio disponibile
								if (str(ep.number) == str(episode["num"]) and not anime["absolute"]) or (str(ep.number) == str(episode["abs"]) and anime["absolute"]): 
									logger.info(txt.EPISODE_AVAILABLE_LOG)
									logger.warning(txt.EPISODE_DOWNLOAD_LOG.format(season=episode["season"], episode=episode["num"]))

									title = f'{anime["title"]} - S{episode["season"]}E{episode["num"]}'

									file = ep.download(title, DOWNLOAD_FOLDER)
									if file: 
										logger.info(txt.DOWNLOAD_COMPLETED_LOG)


										if SETTINGS["MoveEp"]:
											logger.info(txt.EPISODE_SHIFT_LOG.format(season=episode["season"], episode=episode["num"], folder=anime["path"]))
											if movefile(os.path.join(DOWNLOAD_FOLDER,file), anime["path"]): 
												logger.info(txt.EPISODE_SHIFT_DONE_LOG)

											logger.info(txt.ANIME_REFRESH_LOG.format(anime=anime["title"]))
											sonarr.rescanSerie(anime["ID"])

											if SETTINGS["RenameEp"]:
												logger.info(txt.EPISODE_RENAME_LOG)
												for i in range(5): # Fa 5 tentativi
													try:
														time.sleep(1)
														epFileId = sonarr.getEpisodeFileID(episode["ID"])
													except KeyError:
														continue
													else:
														sonarr.renameEpisode(anime["ID"], epFileId)
														logger.info(txt.EPISODE_RENAME_DONE_LOG)
														break
												else:
													logger.warning(txt.EPISODE_RENAME_ERROR_LOG)

											if None not in (CHAT_ID, BOT_TOKEN):
												logger.info(txt.SEND_TELEGRAM_MESSAGE_LOG)
												telegram.sendMessage(txt.TELEGRAM_MESSAGE.format(title=anime["title"], season=episode["season"], episode=episode["num"], episodeTitle=episode["title"]))

									break
							else:
								logger.info(txt.EPISODE_UNAVAILABLE_LOG)

					
					except requests.exceptions.RequestException as res_error:
						logger.warning(txt.CONNECTION_ERROR_LOG.format(res_error=res_error))
					except aw.AnimeNotAvailable as info:
						logger.warning(txt.WARNING_STATE_LOG.format(warning=info))
					except aw.ServerNotSupported as warning:
						logger.error(txt.ERROR_STATE_LOG.format(error=warning))
					except aw.DeprecatedLibrary as dev:
						logger.critical(txt.CRITICAL_STATE_LOG.format(critical=dev))
					finally:
						logger.warning(f"\n{txt.DIVIDER_LOG}\n")

		else:
			logger.info(f"\n{txt.NO_EPISODES}\n")

	except requests.exceptions.RequestException as res_error:
		logger.error(txt.CONNECTION_ERROR_LOG.format(res_error=res_error))	
	except Exception as error:
		logger.exception(txt.EXCEPTION_STATE_LOG.format(exception=error))

	nextStart = time.strftime("%d %b %Y %H:%M:%S", time.localtime(time.time() + SETTINGS["ScanDelay"]*60))
	logger.warning(f"\n{txt.END_BLOCK_LOG.format(time=nextStart)}\n")


