#!/usr/bin/python3

import schedule
import time
import threading
import requests


from other.constants import SONARR_URL, API_KEY, VERSION
import other.texts as txt
from utility.settings import Settings
import utility.logger as log
from job import job

from app import app


def main():
	log.logger.warning(txt.START_LOG.format(time=time.strftime('%d %b %Y %H:%M:%S'), version=VERSION) + '\n')
	Settings.refresh = refresh # aggiornamento metodo di Settings per il refresh delle impostazioni


	if SONARR_URL is None:
		log.logger.warning(txt.SONARR_URL_ERROR_LOG + '\n')
	else:
		log.logger.info(txt.SONARR_URL_CHECK_LOG.format(sonar_url=SONARR_URL) + '\n')
	if API_KEY is None:
		log.logger.warning(txt.API_KEY_ERROR_LOG + '\n')
	else:
		log.logger.info(txt.API_KEY_CHECK_LOG.format(api_key=API_KEY) + '\n')

	if None not in (SONARR_URL, API_KEY):

		log.logger.info('\n' + txt.SETTINGS_SCAN_DELAY_LOG.format(delay= Settings.data['ScanDelay']) + '\n')
		log.logger.info(txt.SETTINGS_MOVE_EPISODE_LOG.format(status='ON' if Settings.data['MoveEp'] else 'OFF') + '\n')
		log.logger.info(txt.SETTINGS_RENAME_EPISODE_LOG.format(status='ON' if Settings.data['RenameEp'] else 'OFF') + '\n')
		log.logger.info(txt.SETTINGS_AUTO_BIND_LINK_LOG.format(status='ON' if Settings.data['AutoBind'] else 'OFF') + '\n')
		log.logger.info(txt.SETTINGS_LOG_LEVEL_LOG.format(level=Settings.data['LogLevel']) + '\n')

		log.logger.info('\n' + txt.START_SERVER_LOG + '\n')
		job_thread = threading.Thread(target=server)
		job_thread.start()

		schedule.every(Settings.data["ScanDelay"]).minutes.do(job).run() # Fa una prima esecuzione e poi lo imposta per la ripetizione periodica

# Refresh settings ###########################################

def refresh(self, silent=False):
	"""
	Aggiorna le impostazioni a livello globale.
	"""
	if not silent:
		log.logger.info(txt.SEPARATOR_LOG + '\n')
		log.logger.info(txt.SETTINGS_UPDATED_LOG + '\n')

		log.logger.info('\n' + txt.SETTINGS_SCAN_DELAY_LOG.format(delay= self.data['ScanDelay']) + '\n')
		log.logger.info(txt.SETTINGS_MOVE_EPISODE_LOG.format(status='ON' if self.data['MoveEp'] else 'OFF') + '\n')
		log.logger.info(txt.SETTINGS_RENAME_EPISODE_LOG.format(status='ON' if self.data['RenameEp'] else 'OFF') + '\n')
		log.logger.info(txt.SETTINGS_AUTO_BIND_LINK_LOG.format(status='ON' if self.data['AutoBind'] else 'OFF') + '\n')
		log.logger.info(txt.SETTINGS_LOG_LEVEL_LOG.format(level=self.data['LogLevel']) + '\n')

		log.logger.info(txt.SEPARATOR_LOG + '\n')

	log.logger.setLevel(self.data["LogLevel"])
	log.message.setLevel(self.data["LogLevel"])
	schedule.clear()
	schedule.every(self.data["ScanDelay"]).minutes.do(job)
 
#############################################################################################


def server():
	app.run(debug=False, host='0.0.0.0', use_reloader=False)	

if __name__ == '__main__':
	main()
	while True:
		schedule.run_pending()
		time.sleep(1)