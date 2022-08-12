import logging, logging.handlers
import requests
import time
import os
import subprocess


from app import socketio
import utility.settings as sett
import utility.connections as conn


class MySocketHandler(logging.handlers.SocketHandler):
	def __init__(self, host='localhost', port=None):
		super().__init__(host=host, port=port)

		self.last_pos = 0
	
	def emit(self, record):
		socketio.emit("log", record.msg)

class MyConnectionsHandler(logging.StreamHandler):	
	def emit(self, record):
		for connection in conn.Connections.data:
			if connection["active"]:
				script = os.path.join("connections", connection["script"])
				if os.path.isfile(script):
					subprocess.check_call([script, record.msg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# FORMATTERS ###########################################

default_formatter = logging.Formatter('%(message)s')

# HANDLERS ###########################################

stream_handler = logging.StreamHandler()
stream_handler.terminator = ''
stream_handler.setFormatter(default_formatter)

file_handler = logging.FileHandler(filename='log.log')
file_handler.terminator = ''
file_handler.setFormatter(default_formatter)

socket_handler = MySocketHandler()
socket_handler.terminator = ''
socket_handler.setFormatter(default_formatter)

connections_handler = MyConnectionsHandler()
connections_handler.terminator = ''
connections_handler.setFormatter(default_formatter)

# LOGGERS ###########################################

logger = logging.getLogger('mylogger')
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.addHandler(socket_handler)
logger.setLevel(sett.Settings.data["LogLevel"])
logger.propagate = True

message = logging.getLogger('message')
message.addHandler(connections_handler)
message.setLevel(sett.Settings.data["LogLevel"])
message.propagate = True


