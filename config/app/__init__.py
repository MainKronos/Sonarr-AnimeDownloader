from flask import *

from .app import app, socketio
from . import api

import logging
logging.getLogger('schedule').setLevel(logging.CRITICAL)
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