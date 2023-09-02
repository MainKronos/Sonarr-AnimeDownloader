import os
import pathlib

SONARR_URL = os.getenv('SONARR_URL')
"""URL di Sonarr"""

API_KEY = os.getenv('API_KEY')
"""Chiave API di Sonarr"""

VERSION = os.getenv('VERSION')
"""Versione programma"""

DOWNLOAD_FOLDER = pathlib.Path('/downloads')
"""Cartella in cui verranno scaricati gli episodi"""

DATABASE_FOLDER = pathlib.Path("/src/database")
"""Cartella che contiene i file con le varie configurazioni"""

SCRIPT_FOLDER = pathlib.Path("/src/script")
"""Cartella che contiene i vari script (Connections)"""

LOGGER = "mylogger"
"""Nome del logger"""