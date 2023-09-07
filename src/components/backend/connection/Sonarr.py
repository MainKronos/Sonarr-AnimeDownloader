import httpx
from ..core import Constant as ctx

class Sonarr:
	"""
	Collegamento con le API di Sonarr.
	Maggiori info: https://sonarr.tv/docs/api/
	"""

	def __init__(self, url:str, api_key:str) -> None:
		self.log = ctx.LOGGER
		self.client = httpx.Client(
			base_url=f"{url}/api/v3",
			headers={
				'X-Api-Key':api_key
			}
		)

		# Controlla che il sito sia raggiungibile e che la api_key sia valida
		self.systemStatus().raise_for_status()
	
	def systemStatus(self) -> httpx.Response:
		"""
		Controlla lo stato del sistema.

		Returns:
		  La risposta HTTP
		"""
		return self.client.get("/system/status")
	
	def wantedMissing(self, n:int=20, page:int=1) -> httpx.Response:
		"""
		Ottiene le informazioni riguardanti gli episodi mancanti.

		Args:
		  n: numero di episodi massimi richiesti
		  page: pagina da scaricare
		
		Returns:
		  La risposta HTTP
		"""
		return self.client.get("/wanted/missing", params={
			"includeSeries": True,
			"pageSize": n,
			"page": page,
			"sortKey": "airDateUtc"
		})
	
	def episode(self, epId:int) -> httpx.Response:
		"""
		Ottiene informazioni su un episodio con id `epId`.

		Args:
		  epId: ID dell'episodio
		
		Returns:
		  La risposta HTTP
		"""
		return self.client.get(f"/episode/{epId}")
	
	def queue(self) -> httpx.Response:
		"""
		Ottiene la lista di episodi che sono nella coda di download.

		Returns:
		  La risposta HTTP
		"""
		return self.client.get("/queue", params={
			"includeUnknownSeriesItems": True,
			"includeSeries": True,
			"includeEpisode": True
		})

	def serie(self, seriesId:int) -> httpx.Response:
		"""
		Ottiene informazioni su una serie.

		Args:
		  seriesId: ID della Serie

		Returns:
		  La risposta HTTP
		"""
		return self.client.get(f"/series/{seriesId}")
	
	def tags(self) -> httpx.Response:
		"""
		Ottiene la lista dei tag.

		Returns:
		  La risposta HTTP
		"""
		return self.client.get("/tag")
	
	### COMMAND
	
	def commandRescanSeries(self, seriesId:int) -> httpx.Response:
		"""
		Esegue un rescan della serie con id `seriesId`.

		Args:
		  seriesId: ID della Serie

		Returns:
		  La risposta HTTP
		"""
		return self.client.post("/command", json={
			"name": "RescanSeries",
			"seriesId": seriesId
		})
	
	def commandRenameSerie(self, seriesIds:list[int]) -> httpx.Response:
		"""
		Rinomina gli episodi delle serie con id in `seriesIds`.

		Args:
		  seriesIds: ID delle Serie

		Returns:
		  La risposta HTTP
		"""
		return self.client.post("/command", json={
			"name": "RenameSeries",
			"seriesIds": seriesIds
		})
	
	def commandRenameFiles(self, seriesId:int, files:list[int]) -> httpx.Response:
		"""
		Rinomina i file appartenenti ad una serie.

		Args:
		  seriesIds: ID delle Serie
		  files: ID dei file

		Returns:
		  La risposta HTTP
		"""
		return self.client.post("/command", json={
			"name": "RenameFiles",
			"seriesId": seriesId,
			"files": files
		})