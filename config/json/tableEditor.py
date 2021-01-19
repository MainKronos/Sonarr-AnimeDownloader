import json
import os


def main():

	if not os.path.exists("table.json"):
		f = open("table.json", 'w')
		f.write(json.dumps(list([]), indent=4))
		f.close()

	while True:

		f = open("table.json", 'r')
		table = json.loads(f.read())
		f.close()

		SonarrTitle = input("Inserire titolo anime di Sonarr: ")
		season = input("Inserire la stagione dell'anime {}: ".format(SonarrTitle))
		AnimeWorldlink = input("Inserire il link della serie di AnimeWorld: ")

		for anime in table:
			if SonarrTitle == anime["title"]: # Se esiste già l'anime nella tabella

				if season in anime["seasons"]: # Se esiste già la stagione
					anime["seasons"][season].append(AnimeWorldlink) # aggiunge un'altro link
					print(f"\n-> È stata aggiunto un altro link per la stagione {season} della serie {SonarrTitle}.")
				else:
					anime["seasons"][season] = [AnimeWorldlink] # inizializza una nuova stagione
					print(f"\n-> È stata aggiunta la stagione {season} per la serie {SonarrTitle}.")

				break
		else: # se non è stato trovato nessun anime
			table.append({
				"title": SonarrTitle,
				"seasons": {season: [AnimeWorldlink]}
			})
			print(f"\n-> È stata aggiunta la serie {SonarrTitle}.")

		table.sort(key=myOrder) # Riordina la tabella in ordine alfabetico

		f = open("table.json", 'w')
		f.write(json.dumps(table, indent=4))
		f.close()


		print("\n---------------------------------------------\n")

def myOrder(serieInfo):
	return serieInfo["title"]

if __name__ == '__main__':
	main()