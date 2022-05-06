#!/usr/bin/python3

from importlib_metadata import version
import schedule
import time
import threading
import requests

from logger import logger, telegram
from constants import SONARR_URL, API_KEY, CHAT_ID, BOT_TOKEN, SETTINGS, VERSION
import texts as txt

from anime_downloader import job
from app import app


def main():
	logger.warning(txt.START_LOG.format(time=time.strftime('%d %b %Y %H:%M:%S'), version=VERSION) + '\n')

	if SONARR_URL is None:
		logger.warning(txt.SONARR_URL_ERROR_LOG + '\n')
	else:
		logger.debug(txt.SONARR_URL_CHECK_LOG.format(sonar_url=SONARR_URL) + '\n')
	if API_KEY is None:
		logger.warning(txt.API_KEY_ERROR_LOG + '\n')
	else:
		logger.debug(txt.API_KEY_CHECK_LOG.format(api_key=API_KEY) + '\n')
	if CHAT_ID is None:
		logger.debug(txt.CHAT_ID_ERROR_LOG + '\n')
	else:
		logger.debug(txt.CHAT_ID_CHECK_LOG.format(chat_id=CHAT_ID) + '\n')
	if BOT_TOKEN is None:
		logger.debug(txt.BOT_TOKEN_ERROR_LOG + '\n')
	else:
		logger.debug(txt.BOT_TOKEN_CHECK_LOG.format(bot_token=BOT_TOKEN) + '\n')

	if None not in (SONARR_URL, API_KEY):

		logger.info('\n' + txt.SETTINGS_SCAN_DELAY_LOG.format(delay=SETTINGS['ScanDelay']) + '\n')
		logger.info(txt.SETTINGS_MOVE_EPISODE_LOG.format(status='ON' if SETTINGS['MoveEp'] else 'OFF') + '\n')
		logger.info(txt.SETTINGS_RENAME_EPISODE_LOG.format(status='ON' if SETTINGS['RenameEp'] else 'OFF') + '\n')
		logger.info(txt.SETTINGS_AUTO_BIND_LINK_LOG.format(status='ON' if SETTINGS['AutoBind'] else 'OFF') + '\n')
		logger.info(txt.SETTINGS_LOG_LEVEL_LOG.format(level=SETTINGS['LogLevel']) + '\n')

		logger.info('\n' + txt.START_SERVER_LOG + '\n')
		job_thread = threading.Thread(target=server)
		job_thread.start()

		job() # Fa una prima esecuzione e poi lo imposta per la ripetizione periodica
		schedule.every(SETTINGS['ScanDelay']).minutes.do(job)


def server():
	app.run(debug=False, host='0.0.0.0', use_reloader=False)	

if __name__ == '__main__':
	main()
	while True:
		schedule.run_pending()
		time.sleep(1)