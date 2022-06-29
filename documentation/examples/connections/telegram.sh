#!/bin/sh


################################################################

BOT_TOKEN="codicecodicecodicecodice"
CHAT_ID="codicecodice"

################################################################

curl -X POST \
   -H 'Content-Type: application/json' \
   -H 'authority: api.telegram.org' \
   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
   -H 'accept-language: it,it-IT;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
   -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37' \
   -d "{\"chat_id\": \"$CHAT_ID\", \"text\": \"$1\"}" \
   https://api.telegram.org/bot$BOT_TOKEN/sendMessage?parse_mode=Markdown \
   --compressed --silent --output /dev/null