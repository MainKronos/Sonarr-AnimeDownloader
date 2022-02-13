import logging.config

from constants import SETTINGS

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
            'formatter': 'default_formatter'
        },
		'file_handler': {
			'class': 'logging.FileHandler',
			'formatter': 'default_formatter',
			'filename': 'log.log',
			'mode': 'w',
		}
    },
    'loggers': {
        'mylogger': {
            'handlers': ['stream_handler','file_handler'],
            'level': SETTINGS["LogLevel"],
            'propagate': True
        }
    }
})

logger = logging.getLogger('mylogger')