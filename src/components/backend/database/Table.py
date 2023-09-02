from .Database import Database

class Table(Database):
	def fix(self) -> None:
		if not self.db.exists() or self.db.stat().st_size == 0:
			self.write([])
	
	