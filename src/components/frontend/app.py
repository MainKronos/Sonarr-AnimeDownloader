from flask import *
from flask_socketio import *
import logging, sys
import logging.handlers
from datetime import datetime

from .api import loadAPI

from ..backend import Core

def Frontend(core:Core) -> Flask:
	"""
	Costruisce il frontend.

	Args:
	  core: il core del programma
	
	Returns:
	  Il fronted
	"""

	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'secret!'
	app.config['CORE'] = core

	socketio = SocketIO(app, logger=True, async_handlers=False)

	@socketio.on('connected')
	def handler(data):
		pass

	setupLog(app, socketio)
	loadRoute(app)
	loadAPI(app)

	return app

def setupLog(app:Flask, socketio:SocketIO):
	core:Core = app.config['CORE']
	
	sys.modules['flask.cli'].show_server_banner = lambda *x: None
	logging.getLogger('urllib3.util.retry').setLevel(logging.CRITICAL)
	logging.getLogger('urllib3.util').setLevel(logging.CRITICAL)
	logging.getLogger('urllib3').setLevel(logging.CRITICAL)
	logging.getLogger('urllib3.connection').setLevel(logging.CRITICAL)
	logging.getLogger('urllib3.response').setLevel(logging.CRITICAL)
	logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)
	logging.getLogger('urllib3.poolmanager').setLevel(logging.CRITICAL)
	logging.getLogger('charset_normalizer').setLevel(logging.CRITICAL)
	logging.getLogger('requests').setLevel(logging.CRITICAL)
	logging.getLogger('engineio.client').setLevel(logging.CRITICAL)
	logging.getLogger('engineio').setLevel(logging.CRITICAL)
	logging.getLogger('engineio.server').setLevel(logging.CRITICAL)
	logging.getLogger('concurrent.futures').setLevel(logging.CRITICAL)
	logging.getLogger('concurrent').setLevel(logging.CRITICAL)
	logging.getLogger('asyncio').setLevel(logging.CRITICAL)
	logging.getLogger('socketio.client').setLevel(logging.CRITICAL)
	logging.getLogger('socketio').setLevel(logging.CRITICAL)
	logging.getLogger('socketio.server').setLevel(logging.CRITICAL)
	logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
	logging.getLogger('bs4.dammit').setLevel(logging.CRITICAL)
	logging.getLogger('bs4').setLevel(logging.CRITICAL)

	class MySocketHandler(logging.handlers.SocketHandler):
		def __init__(self, host='localhost', port=None):
			super().__init__(host=host, port=port)

			self.last_pos = 0
		
		def emit(self, record):
			socketio.emit("log", record.msg)
	
	socket_handler = MySocketHandler()
	socket_handler.setFormatter('%(levelname)-8s %(message)s')
	core.log.addHandler(socket_handler)

	
	def downloadProgress(d):
		"""
		Stampa il progresso di download dell'episodio.
		"""
		
		if int(datetime.timestamp(datetime.now()) - downloadProgress.step ) > 0 or d["percentage"] == 1:
			socketio.emit("download_info", d)
			downloadProgress.step = datetime.timestamp(datetime.now())

	downloadProgress.step = datetime.timestamp(datetime.now())
	core.downloader.connectHook(downloadProgress)

def loadRoute(app:Flask):

	core:Core = app.config['CORE']

	@app.route('/index')
	@app.route('/')
	def index():
		return render_template('index.html', version=core.version)

	@app.route('/settings')
	def settings():
		return render_template('settings.html', sonarr_url=core.sonarr.url, api_key=core.sonarr.api_key, version=core.version)

	@app.route('/log')
	def log():
		return render_template('log.html', version=core.version)