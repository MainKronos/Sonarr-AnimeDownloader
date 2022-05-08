import logging.config

from utility import Settings
from constants import CHAT_ID, BOT_TOKEN
from app import socketio
import requests


class MySocketHandler(logging.handlers.SocketHandler):
	def __init__(self, host='localhost', port=None):
		super().__init__(host=host, port=port)

		self.last_pos = 0
	
	def emit(self, record):
		socketio.emit("log", record.msg)

class TelegramHandler(logging.handlers.HTTPHandler):
	
	def emit(self, record):
		requests.get(self.host + self.url + record.msg)

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default_formatter': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
			'.': {
				'terminator': ''
			}
        },
		'file_handler': {
			'class': 'logging.FileHandler',
			'formatter': 'default_formatter',
			'filename': 'log.log',
			'mode': 'w+',
			'.': {
				'terminator': ''
			}
		},
		'socket_handler': {
			'class': 'logger.MySocketHandler',
			'formatter': 'default_formatter',
			'.': {
				'terminator': ''
			}
		},
		'telegram_handler':{
			'class': 'logger.TelegramHandler',
			'formatter': 'default_formatter',
			'host': 'https://api.telegram.org',
			'url': f'/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&parse_mode=Markdown&text=',
			'method': 'GET'
		}

    },
    'loggers': {
        'mylogger': {
            'handlers': ['stream_handler','file_handler', 'socket_handler'],
            'level': Settings.data["LogLevel"],
            'propagate': True
        },
		'message': {
			'handlers': ['telegram_handler'],
            'level': Settings.data["LogLevel"],
            'propagate': True
		}
    }
})

logger = logging.getLogger('mylogger')
message = logging.getLogger('message')