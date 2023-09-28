#!/bin/sh

################################################################

WEBHOOK_URL="discord_webhook"
USERNAME="username"

################################################################

curl -u $ACCESS_TOKEN: $PUSHBULLET_API \
   -H "Content-Type: application/json" \
   -d "{\"username\": \"$USERNAME\", \"content\": \"$1\"}" \
   $WEBHOOK_URL \ 
   --silent --output /dev/null