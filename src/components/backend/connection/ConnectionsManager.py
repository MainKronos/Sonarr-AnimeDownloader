from ..database import ConnectionsDB

import subprocess

class ConnectionsManager:
	"""Gestisce il comportamento delle connections."""

	def __init__(self, db:ConnectionsDB):
		self.db = db

	def send(self, msg:str) -> None:
		"""
		Invia il messaggio tramite le Connections.

		Args:
		  msg: messaggio da inviare
		"""

		for connection in self.db:
			if not connection['active']: continue
			file = self.db.getPath(connection['name'])
			if not file.is_file(): continue
			subprocess.check_call([file, msg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)