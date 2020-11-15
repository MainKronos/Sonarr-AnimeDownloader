import json
import os


def main():

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

		for row in range(len(table)):
			if table[row]["Sonarr"]["title"] == SonarrTitle and table[row]["Sonarr"]["season"] == season:
				print("L'anime {} (stagione {}) è gia presente, e corrisponde a {}".format(SonarrTitle, season, table[row]["AnimeWorld"]["title"]))
				yn = input("Aggiungere un altro titolo (y/n): ")
				if yn == 'y':
					AnimeWorldTitle = input("Inserire titolo anime di AnimeWorld: ")
					table[row]["AnimeWorld"]["title"].append(AnimeWorldTitle)
					break
				else:
					break
		else:
			AnimeWorldTitle = input("Inserire titolo anime di AnimeWorld: ")

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
	return serieInfo["Sonarr"]["title"] + str(serieInfo["Sonarr"]["season"])


if __name__ == '__main__':
	main()