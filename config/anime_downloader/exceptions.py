
class TableFormattingError(Exception):
	"""Il file table.json è formattato male."""
	def __init__(self):
		self.message = "Errore al file table.json."
		super().__init__(self.message)

class UnauthorizedSonarr(Exception):
	def __init__(self, message):
		super().__init__(message)