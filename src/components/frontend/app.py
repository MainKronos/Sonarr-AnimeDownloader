from flask import *

from other.constants import VERSION, SONARR_URL, API_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

@app.route('/index')
@app.route('/')
def index():
	return render_template('index.html', version=VERSION)

@app.route('/settings')
def settings():
	return render_template('settings.html', sonarr_url=SONARR_URL, api_key=API_KEY, version=VERSION)

@app.route('/log')
def log():
	return render_template('log.html', version=VERSION)