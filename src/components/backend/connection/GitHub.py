import httpx

from ..core import LOGGER

class GitHub:
	"""
	Collegamento con le REST API di GitHub.
	https://docs.github.com/en/rest
	"""

	def __init__(self) -> None:
		self.log = LOGGER
		self.client = httpx.Client(
			base_url="https://api.github.com",
			headers={
				"Accept": "application/vnd.github+json",
				"X-GitHub-Api-Version": "2022-11-28"
			}
		)
	
	def getLatestVersion(self) -> str:
		"""Ritorna il nome dell'ultima versione del progetto."""

		res = self.client.get("/repos/MainKronos/Sonarr-AnimeDownloader/releases/latest")
		res.raise_for_status()
		return res.json()["name"]