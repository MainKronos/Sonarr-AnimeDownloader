import logging.config

from utility import Settings, Connections
from app import socketio
import requests
import time
import os


class MySocketHandler(logging.handlers.SocketHandler):
	def __init__(self, host='localhost', port=None):
		super().__init__(host=host, port=port)

		self.last_pos = 0
	
	def emit(self, record):
		socketio.emit("log", record.msg)

class ConnectionsHandler(logging.StreamHandler):	
	def emit(self, record):
		for connection in Connections.data:
			if connection["active"]:
				script = os.path.join("connections", connection["script"])
				if os.path.isfile(script):
					os.system(f'{script} "{record.msg}"')

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
		'connections_handler':{
			'class': 'logger.ConnectionsHandler'
		}

    },
    'loggers': {
        'mylogger': {
            'handlers': ['stream_handler','file_handler', 'socket_handler'],
            'level': Settings.data["LogLevel"],
            'propagate': True
        },
		'message': {
			'handlers': ['connections_handler'],
            'level': Settings.data["LogLevel"],
            'propagate': True
		}
    }
})

logger = logging.getLogger('mylogger')
message = logging.getLogger('message')