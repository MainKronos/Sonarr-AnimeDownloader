import json
import os


def main():

	fixData()

	while True:

		if not os.path.exists("table.json"):
			f = open("table.json", 'w')
			f.write(json.dumps(list([]), indent=4))
			f.close()

		f = open("table.json", 'r')
		table = json.loads(f.read())
		f.close()

		SonarrTitle = input("Inserire titolo anime di Sonarr: ")
		season = int(input("Inserire la stagione dell'anime {}: ".format(SonarrTitle)))
		AnimeWorldTitle = input("Inserire titolo anime di AnimeWorld: ")

		for row in range(len(table)):
			if table[row]["Sonarr"]["title"] == SonarrTitle and season in table[row]["Sonarr"]["season"]:
				print("L'anime {} (stagione {}) è gia presente, e corrisponde a {}".format(SonarrTitle, season, table[row]["AnimeWorld"]["title"]))
				yn = input(f"Aggiungere il titolo {AnimeWorldTitle} alla lista? (y/n): ")
				if yn == 'y':
					table[row]["AnimeWorld"]["title"].append(AnimeWorldTitle)
					break
				else:
					break

			if table[row]["Sonarr"]["title"] == SonarrTitle and AnimeWorldTitle in table[row]["AnimeWorld"]["title"]:
				print("L'anime {} corrispondente a {} (AnimeWorld) è gia presente".format(SonarrTitle, table[row]["AnimeWorld"]["title"]))
				yn = input(f"Aggiungere la sagione {season} alla lista? (y/n): ")
				if yn == 'y':
					table[row]["Sonarr"]["season"].append(season)
					break
				else:
					break

		else:
			newBlock = {
				"Sonarr": {
					"title": SonarrTitle,
					"season": season
				},
				"AnimeWorld": {
					"title": [AnimeWorldTitle]
				}
			}

			table.append(newBlock)
			print("L'anime {} (stagione {}) è stato aggiunto correttamente.".format(SonarrTitle, season))

		table.sort(key=myOrder)

		f = open("table.json", 'w')
		f.write(json.dumps(table, indent=4))
		f.close()


		print("\n---------------------------------------------\n")

def myOrder(serieInfo):
	return serieInfo["Sonarr"]["title"]

def fixData():
	f = open("table.json", 'r')
	table = json.loads(f.read())
	f.close()

	for row in table:
		if not isinstance(row["Sonarr"]["season"], list):
			row["Sonarr"]["season"] = [row["Sonarr"]["season"]]

	f = open("table.json", 'w')
	f.write(json.dumps(table, indent=4))
	f.close()

if __name__ == '__main__':
	main()