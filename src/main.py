#!/usr/bin/python3
from components import Core, Frontend
import threading

def main():
	# Carico il core
	core = Core()
	
	# Cario la pagina web
	app = Frontend(core)

	# Avvio la pagina web
	threading.Thread(target=server, args=[app])

	# Avvio il programma
	core.start()

	# Attendo che venga sollevata un eccezione non prevista
	core.join()

def server(app):
	app.run(debug=False, host='0.0.0.0', use_reloader=False)

if __name__ == '__main__':
	main()