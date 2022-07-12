#!/bin/sh

USER_NAME="dockeruser"

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

chown "$USER_NAME":"$USER_NAME" /downloads -R
chown "$USER_NAME":"$USER_NAME" /script -R

chmod 777 /downloads -R
chmod 777 /script -R

su $USER_NAME -c "python3 -u /script/main.py"