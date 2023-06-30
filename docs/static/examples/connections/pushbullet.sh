#!/bin/sh

################################################################

ACCESS_TOKEN="codecodecodecode"
PUSHBULLET_API="https://api.pushbullet.com/v2/pushes"

################################################################

curl -u $ACCESS_TOKEN: $PUSHBULLET_API \
   -d type=note \
   -d title="Sonarr - Anime Downloader" \
   -d body="$1" \
   --silent --output /dev/null
