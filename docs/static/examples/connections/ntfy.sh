#!/bin/sh

################################################################

BASE_URL="http://ntfy.sh" # URL del servizio ntfy (può essere anche self-hosted)
TOKEN="12345676890abcdefg" # Token del topic ntfy
TOPIC="your-ntfy-topic" # Nome del topic ntfy
PRIORITA="low" # high, normal, low
ICONA="http://path/to/icon.png" # URL di un'icona
TAG="loudspeaker,anime,new-download" # I tuoi tags (la prima, secondo le specifiche, sarà l'emoji della notifica)
MESSAGGIO="$1"

################################################################

curl -X POST "$BASE_URL/$TOPIC" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Title: $TITOLO" \
     -H "Priority: $PRIORITA" \
     -H "Icon: $ICONA" \
     -H "Tag: $TAG" \
     -H "Markdown: yes" \
     -d "$MESSAGGIO" \
     --silent --output /dev/null