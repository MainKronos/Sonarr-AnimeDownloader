import os, logging
import pathlib

SONARR_URL:str = os.getenv('SONARR_URL')
"""URL di Sonarr"""

ANIMEWORLD_URL:str = os.getenv('ANIMEWORLD_URL', 'https://www.animeworld.ac/')
"""URL di AnimeWorld"""

API_KEY:str = os.getenv('API_KEY')
"""Chiave API di Sonarr"""

VERSION:str = os.getenv('VERSION')
"""Versione programma"""

DOWNLOAD_FOLDER:pathlib.Path = pathlib.Path('/downloads')
"""Cartella in cui verranno scaricati gli episodi"""

DATABASE_FOLDER:pathlib.Path = pathlib.Path("/src/database")
"""Cartella che contiene i file con le varie configurazioni"""

SCRIPT_FOLDER:pathlib.Path = pathlib.Path("/src/script")
"""Cartella che contiene i vari script (Connections)"""

LOGGER = logging.getLogger("mylogger")
"""Nome del logger"""