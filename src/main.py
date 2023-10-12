#!/usr/bin/python3
from components import Core, API
import threading
import uvicorn

def main():
	# Carico il core
	core = Core()
	
	# Cario la pagina web
	app = API(core)

	# Avvio la pagina web
	threading.Thread(target=server, args=[app], daemon=True).start()

	# Avvio il programma
	core.start()

	# Attendo che venga sollevata un eccezione non prevista
	core.join()

def server(app):
	uvicorn.run(app, port=5000, host='0.0.0.0', log_level='critical')

if __name__ == '__main__':
	main()