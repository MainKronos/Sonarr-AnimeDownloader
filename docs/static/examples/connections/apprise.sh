#!/bin/sh

################################################################

BASE_URL="http://apprise/notify" # URL del servizio apprise (può essere anche self-hosted)
TOPIC="your-apprise-topic" # Nome del topic 
MESSAGGIO="$1"

################################################################

curl -X POST \
   -F "body=$MESSAGGIO" \
   -F "format=markdown" \
   "$BASE_URL/$TOPIC" \
   --compressed --silent --output /dev/null