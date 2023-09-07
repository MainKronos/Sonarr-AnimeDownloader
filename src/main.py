#!/usr/bin/python3
from components import Core

def main():
	core = Core()
	
	core.start()

	core.join()


if __name__ == '__main__':
	main()