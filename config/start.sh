#!/bin/sh

set -e

PUID=${PUID:-1000}
PGID=${PGID:-1000}

groupmod -o -g "$PGID" "$USER_NAME"
usermod -o -u "$PUID" "$USER_NAME"

echo '
-------------------------------------
GID/UID
-------------------------------------'
echo "
User uid:    $(id -u "$USER_NAME")
User gid:    $(id -g "$USER_NAME")
-------------------------------------
"

touch /script/json/settings.json
touch /script/json/table.json

chown "$USER_NAME":"$USER_NAME" /script -R
chmod 777 /script -R

pip3 install --upgrade --no-cache-dir --disable-pip-version-check --quiet animeworld

su $USER_NAME -c "python3 -u /script/main.py"