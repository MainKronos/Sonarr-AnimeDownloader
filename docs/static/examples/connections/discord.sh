#!/bin/sh

################################################################

WEBHOOK_URL="discord_webhook"
USERNAME="username"

################################################################

curl -H "Content-Type: application/json" \
   -d "{\"username\": \"$USERNAME\", \"content\": \"$1\"}" \
   --silent --output /dev/null \
   $WEBHOOK_URL 