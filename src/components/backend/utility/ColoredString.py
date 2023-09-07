from typing import Literal

class ColoredString:
	"""
	Gestione stringhe di testo colorate con il formato ansi.\\
	https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
	"""

	BLACK = "\x1b[0;30m"
	RED = "\x1b[0;30m"
	GREEN = "\x1b[0;32m"
	YELLOW = "\x1b[0;33m"
	BLUE = "\x1b[0;34m"
	PURPLE = "\x1b[0;35m"
	CYAN = "\x1b[0;36m"
	WHITE = "\x1b[0;37m"
	RESET = "\x1b[0m"


	@staticmethod
	def black(string:str):
		return f"\x1b[0;30m{string}\x1b[0m"
	
	@staticmethod
	def red(string:str):
		return f"\x1b[0;31m{string}\x1b[0m"
	
	@staticmethod
	def green(string:str):
		return f"\x1b[0;32m{string}\x1b[0m"
	
	@staticmethod
	def yellow(string:str):
		return f"\x1b[0;33m{string}\x1b[0m"
	
	@staticmethod
	def blue(string:str):
		return f"\x1b[0;34m{string}\x1b[0m"
	
	@staticmethod
	def purple(string:str):
		return f"\x1b[0;35m{string}\x1b[0m"
	
	@staticmethod
	def cyan(string:str):
		return f"\x1b[0;36m{string}\x1b[0m"
	
	@staticmethod
	def white(string:str):
		return f"\x1b[0;37m{string}\x1b[0m"