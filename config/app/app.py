from flask import *

from constants import VERSION, SONARR_URL, API_KEY, CHAT_ID, BOT_TOKEN

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
	return render_template('index.html', version=VERSION)

@app.route('/settings')
def settings():
	return render_template('settings.html', sonarr_url=SONARR_URL, api_key=API_KEY, chat_id=CHAT_ID, bot_token=BOT_TOKEN, version=VERSION)

@app.route('/log')
def log():
	return render_template('log.html', version=VERSION)