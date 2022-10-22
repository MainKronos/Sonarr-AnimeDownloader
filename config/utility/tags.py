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
	def toggle(self, name:str):

		log = f"Il Tag {name} è stato "

		tags = self.data

		for tag in tags:
			if tag["name"] == name:
				log += "disabilitato." if tag["active"] else "attivato."
				tag["active"] = not tag["active"]
				break
		else:
			return f"Non è stato trovato nessun Tag con il nome {name}."

		self.write(tags)
		return log
	
	@classmethod
	def remove(self, name:str):
		
		deleting = None
		tags = self.data

		for tag in tags:
			if tag["name"] == name:
				deleting = tag
				break
		else:
			return f"Non è stato trovato nessun Tag {name}."

		tags.remove(deleting)

		self.write(tags)
		return f"Il Tag {name} è stato rimosso."
	
	@classmethod
	def add(self, name:str, inclusive:str, active:bool, availableTags:list):
		if self.isValid(name):
			tags = self.data

			for tag in availableTags:
				if tag["label"] == name: 
					tags.append({
						"id": tag["id"],
						"name": name,
						"inclusive": inclusive,
						"active": active
					})
					self.write(tags)
					return f"Il tag {name} è stato aggiunto."
			else:
				return f"Il Tag {name} non esiste su Sonarr."
		else:
			return f"È gia presente un Tag {name}."


	@classmethod
	def isValid(self, tag_name:str):
		for tag in self.data:
			if tag["name"] == tag_name:
				return False
		else:
			return True

	@classmethod
	def write(self, tags:List):
		"""
		Sovrascrive le Connections con le nuove informazioni.
		"""

		for i in range(len(tags)):
			for j in range(len(tags)):
				if i==j: continue

				if tags[i]["name"] == tags[j]["name"]: return False

		with open(self.file, 'w') as f:
			f.write(json.dumps(tags, indent=4))
		
		return True

	@classmethod
	def updateAvailableSonarrTags(self, availableTags):
		"""
		Aggiorno i tag attuali con quelli disponibili su Sonarr
		"""

		tags = Tags.data
		for tag in tags:
			for avTag in availableTags:
				if tag["id"] == avTag["id"]: break
			else:
				tag["active"] = False

		self.write(tags)
		return True

