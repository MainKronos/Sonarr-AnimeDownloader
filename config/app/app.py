from flask import *
from flask_socketio import *

from constants import VERSION, SONARR_URL, API_KEY, CHAT_ID, BOT_TOKEN

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=False, async_handlers=False)

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
	