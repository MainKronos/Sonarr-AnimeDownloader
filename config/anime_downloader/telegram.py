import requests

from constants import BOT_TOKEN, CHAT_ID
import texts as txt

def sendMessage(info):
	text = txt.TELEGRAM_MESSAGE.format(
		title=info["SonarrTitle"], season=str(info["season"]), episode=str(info["episode"]), episodeTitle=info["episodeTitle"]
	)

	url ="https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(BOT_TOKEN, text, CHAT_ID)
	requests.get(url)