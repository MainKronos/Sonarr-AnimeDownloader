import os

SONARR_URL = os.getenv('SONARR_URL') # Indirizzo ip + porta di sonarr
API_KEY = os.getenv('API_KEY') # Chiave api di sonarr
VERSION = os.getenv('VERSION') # versione

DOWNLOAD_FOLDER = '/downloads'