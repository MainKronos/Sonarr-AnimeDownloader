from typing import Dict, List
import json
import os

from .classproperty import classproperty

class Tags:
	file = "json/tags.json"

	@classproperty
	def data(self) -> List[Dict]:
		"""
		Lista di dizionari contenente tutte le informazioni.
		"""

		if os.path.exists(self.file) and os.path.getsize(self.file) > 0:
			try:
				with open(self.file, 'r') as f:
					return json.loads(f.read())
			except json.JSONDecodeError:
				pass
		
		self.write([])
		return []

	@classmethod
	def toggle(self, tag_label:str):

		log = f"La Connection {tag_label} è stata "

		tags = self.data

		for tag in tags:
			if tag["label"] == tag_label:
				file = os.path.join("connections", tag["script"])
				if os.path.isfile(file) or tag["active"]:
					log += "spenta." if tag["active"] else "accesa."
					tag["active"] = not tag["active"]
					break
				else:
					return f"Il file {tag_label} non esiste."
		else:
			return f"Non è stato trovato nessuna Tag con il nome {tag_label}."

		self.write(tags)
		return log
	
	@classmethod
	def remove(self, connection_name:str):
		
		conn = None
		connections = self.data

		for connection in connections:
			if connection["name"] == connection_name:
				conn = connection
				break
		else:
			return f"Non è stato trovato nessuna Connection con il nome {connection_name}."

		connections.remove(conn)

		self.write(connections)
		return f"La Connection {connection_name} è stata rimossa."
	
	@classmethod
	def add(self, name:str, script:str, active:bool):
		if self.isValid(name):
			connections = self.data
			connections.append({
				"name": name,
				"script": script,
				"active": active
			})
			self.write(connections)
			return f"La Connection {name} è stata aggiunta."
		else:
			return f"È gia presente una Connection con il nome {name}."


	@classmethod
	def isValid(self, name:str):
		for connection in self.data:
			if connection["name"] == name:
				return False
		else:
			return True

	@classmethod
	def write(self, connections:List):
		"""
		Sovrascrive le Connections con le nuove informazioni.
		"""

		for i in range(len(connections)):
			for j in range(len(connections)):
				if i==j: continue

				if connections[i]["name"] == connections[j]["name"]: return False

		with open(self.file, 'w') as f:
			f.write(json.dumps(connections, indent=4))
		
		return True


