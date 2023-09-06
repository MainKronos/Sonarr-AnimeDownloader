from typing import Literal

colors = ["black", "red", "green", "yellow", "blue", "purple", "cyan", "white"]

class ColoredString(str):
	"""
	Gestione stringhe di testo colorate con il formato ansi.
	https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
	"""

	def __init__(self, string:str, color:Literal["black","red","green","yellow","blue","purple","cyan","white"] = "") -> None:
		super().__init__(string)

		if color == "black": self.black()
		elif color == "red": self.red()
		elif color == "green": self.green()
		elif color == "yellow": self.yellow()
		elif color == "blue": self.blue()
		elif color == "purple": self.purple()
		elif color == "cyan": self.cyan()
		elif color == "white": self.white()
		else: self.color = ""
	
	def __str__(self) -> str:
		return self.color + super().__str__() + '\x1b[0m'
	
	def black(self):
		self.color = "\x1b[0;30m"
		return self
	
	def red(self):
		self.color = "\x1b[0;31m"
		return self
	
	def green(self):
		self.color = "\x1b[0;32m"
		return self
	
	def yellow(self):
		self.color = "\x1b[0;33m"
		return self
	
	def blue(self):
		self.color = "\x1b[0;34m"
		return self
	
	def purple(self):
		self.color = "\x1b[0;35m"
		return self
	
	def cyan(self):
		self.color = "\x1b[0;36m"
		return self
	
	def white(self):
		self.color = "\x1b[0;37m"
		return self
	
	def default(self):
		self.color = ""
		return self
	
ColoredString(s,)