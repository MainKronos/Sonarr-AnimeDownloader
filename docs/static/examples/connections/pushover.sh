#!/bin/sh

################################################################

APP_TOKEN="codecodecodecode"
USER_KEY="codecodecodecodecodecode"

################################################################

curl -s \
  --form-string "token=$APP_TOKEN" \
  --form-string "user=$USER_KEY" \
  --form-string "message=$1" \
  --silent --output /dev/null \
  "https://api.pushover.net/1/messages.json"