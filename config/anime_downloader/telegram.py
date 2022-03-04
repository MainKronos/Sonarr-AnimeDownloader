import requests

from constants import BOT_TOKEN, CHAT_ID

def sendMessage(msg):
	url ="https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(BOT_TOKEN, msg, CHAT_ID)
	requests.get(url)