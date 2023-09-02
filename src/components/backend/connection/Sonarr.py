import httpx

class Sonarr:
	"""
	Collegamento con le API di Sonarr.
	Maggiori info: https://sonarr.tv/docs/api/
	"""

	def __init__(self, url:str, api_key:str) -> None:
		self.client = httpx.Client(headers={'X-Api-Key':api_key})
		self.url = url

		# Controlla che il sito sia raggiungibile e che la api_key sia valida
		self.systemStatus().raise_for_status()
	
	def systemStatus(self) -> httpx.Response:
		"""
		Controlla lo stato del sistema.

		Returns:
		  La risposta HTTP
		"""
		url = f"{self.url}/api/v3/system/status"
		return self.client.get(url)
	
	def wantedMissing(self, n:int=20) -> httpx.Response:
		"""
		Ottiene le informazioni riguardanti gli episodi mancanti.

		Args:
		  n: numero di episodi massimi richiesti
		
		Returns:
		  La risposta HTTP
		"""
		url = f"{self.url}/api/v3/wanted/missing"
		return self.client.get(url, params={
			"includeSeries": True,
			"pageSize": n,
			"page": 1,
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

		url = f"{self.url}/api/v3/episode/{epId}"
		return self.client.get(url)
	
	def queue(self) -> httpx.Response:
		"""
		Ottiene la lista di episodi che sono nella coda di download.

		Returns:
		  La risposta HTTP
		"""
		url = f"{self.url}/api/v3/queue"
		return self.client.get(url, params={
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

		url = f"{self.url}/api/v3/series/{seriesId}"
		return self.client.get(url)
	
	def tags(self) -> httpx.Response:
		"""
		Ottiene la lista dei tag.

		Returns:
		  La risposta HTTP
		"""
		url = f"{self.url}/api/v3/tag"
		return self.client.get(url)
	
	### COMMAND
	
	def commandRescanSeries(self, seriesId:int) -> httpx.Response:
		"""
		Esegue un rescan della serie con id `seriesId`.

		Args:
		  seriesId: ID della Serie

		Returns:
		  La risposta HTTP
		"""
		url = f"{self.url}/api/v3/command"
		return self.client.post(url, json={
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
		url = f"{self.url}/api/v3/command"
		return self.client.post(url, json={
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
		url = f"{self.url}/api/v3/command"
		return self.client.post(url, json={
			"name": "RenameFiles",
			"seriesId": seriesId,
			"files": files
		})