from flask import *

from ..backend import Core, LOGGER, VERSION

def CreateFrontend(core:Core) -> Flask:
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'secret!'
	app.config['CORE'] = core

	loadRoute(app)

	return app


def loadRoute(app:Flask):

	core:Core = app.config['CORE']

	@app.route('/index')
	@app.route('/')
	def index():
		return render_template('index.html', version=VERSION)

	@app.route('/settings')
	def settings():
		return render_template('settings.html', sonarr_url=core.sonarr.url, api_key=core.sonarr.api_key, version=VERSION)

	@app.route('/log')
	def log():
		return render_template('log.html', version=VERSION)