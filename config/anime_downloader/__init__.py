import time

import requests
import animeworld as aw
import os

import texts as txt
from logger import logger, message
from constants import DOWNLOAD_FOLDER, VERSION
from utility import Settings

from .functions import converting, fixEps, movefile, downloadProgress, getLatestVersion
from . import sonarr
from .exceptions import UnauthorizedSonarr

def job():
	"""
	Esegue la ricerca degli episodi mancanti, se li trova li scarica.
	"""
	logger.warning('\n' + txt.START_BLOCK_LOG.format(time=time.strftime('%d %b %Y %H:%M:%S')) + '\n')

	latest_version_container = getLatestVersion()
	if VERSION != latest_version_container:
		logger.info('\n' + txt.UPDATE_CONTAINER.format(version=latest_version_container))


	try:
		raw_series = sonarr.getMissingEpisodes()
		if len(raw_series)!=0:
			series = converting(raw_series)

			for anime in series:
				for season in anime["seasons"]:
					logger.warning('\n' + txt.DIVIDER_LOG + '\n\n')
					try:
						logger.warning(txt.ANIME_RESEARCH_LOG.format(anime=anime["title"], season=season["num"]) + '\n')

						results = [aw.Anime(link=x) for x in season["links"]]

						logger.info(txt.EPISODE_RESEARCH_LOG.format(episode=", ".join([x["num"] for x in season["episodes"]])) + '\n')

						episodi = fixEps([x.getEpisodes() for x in results])

						for episode in season["episodes"]:
							logger.info('\n' + txt.CHECK_EPISODE_AVAILABILITY_LOG.format(season=episode["season"], episode=episode["num"]) + '\n')
							for ep in episodi:
								
								# episodio disponibile
								if (str(ep.number) == str(episode["num"]) and not anime["absolute"]) or (str(ep.number) == str(episode["abs"]) and anime["absolute"]): 
									logger.info(txt.EPISODE_AVAILABLE_LOG + '\n')
									logger.warning(txt.EPISODE_DOWNLOAD_LOG.format(season=episode["season"], episode=episode["num"]) + '\n')

									title = f'{anime["title"]} - S{episode["season"]}E{episode["num"]}'

									file = ep.download(title, DOWNLOAD_FOLDER, downloadProgress)
									if file: 
										logger.info(txt.DOWNLOAD_COMPLETED_LOG + '\n')


										if Settings.data["MoveEp"]:
											logger.info(txt.EPISODE_SHIFT_LOG.format(season=episode["season"], episode=episode["num"], folder=anime["path"]) + '\n')
											if movefile(os.path.join(DOWNLOAD_FOLDER,file), anime["path"]): 
												logger.info(txt.EPISODE_SHIFT_DONE_LOG + '\n')

											logger.info(txt.ANIME_REFRESH_LOG.format(anime=anime["title"]) + '\n')
											sonarr.rescanSerie(anime["ID"])

											if Settings.data["RenameEp"]:
												logger.info(txt.EPISODE_RENAME_LOG + '\n')
												for i in range(5): # Fa 5 tentativi
													try:
														time.sleep(1)
														epFileId = sonarr.getEpisodeFileID(episode["ID"])
													except KeyError:
														continue
													else:
														sonarr.renameEpisode(anime["ID"], epFileId)
														logger.info(txt.EPISODE_RENAME_DONE_LOG + '\n')
														break
												else:
													logger.warning(txt.EPISODE_RENAME_ERROR_LOG + '\n')

											logger.info(txt.SEND_CONNECTION_MESSAGE_LOG + '\n')
											message.warning(txt.CONNECTION_MESSAGE.format(title=anime["title"], season=episode["season"], episode=episode["num"], episodeTitle=episode["title"]))

									break
							else:
								logger.info(txt.EPISODE_UNAVAILABLE_LOG + '\n')

					
					except requests.exceptions.RequestException as res_error:
						logger.warning(txt.CONNECTION_ERROR_LOG.format(res_error=res_error) + '\n')
					except aw.AnimeNotAvailable as info:
						logger.warning(txt.WARNING_STATE_LOG.format(warning=info) + '\n')
					except aw.ServerNotSupported as warning:
						logger.error(txt.ERROR_STATE_LOG.format(error=warning) + '\n')
					except aw.DeprecatedLibrary as dev:
						logger.critical(txt.CRITICAL_STATE_LOG.format(critical=dev) + '\n')
					finally:
						logger.warning('\n' + txt.DIVIDER_LOG + '\n')

		else:
			logger.info('\n' + txt.NO_EPISODES + '\n')

	except requests.exceptions.RequestException as res_error:
		logger.error(txt.CONNECTION_ERROR_LOG.format(res_error=res_error) + '\n')	
	except UnauthorizedSonarr as e:
		logger.error(str(e) + '\n')	
	except Exception as error:
		logger.exception(txt.EXCEPTION_STATE_LOG.format(exception=error) + '\n')

	nextStart = time.strftime("%d %b %Y %H:%M:%S", time.localtime(time.time() + Settings.data["ScanDelay"]*60))
	logger.warning('\n' + txt.END_BLOCK_LOG.format(time=nextStart) + '\n\n')


