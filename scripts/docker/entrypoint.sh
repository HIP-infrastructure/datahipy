#!/bin/bash

USER=$1
USER_ID=$2

echo -n "Creating user $USER... "
egrep "^$USER" /etc/passwd >/dev/null
if [ $? -eq 0 ]; then
    echo "$USER already exists and has been recreated."
    userdel $USER
fi

useradd --create-home --shell /bin/bash $USER --uid $USER_ID
if [ $? -eq 0 ]; then
    echo "done."
else
    echo "failed."
    exit 1
fi

runuser -u $USER -- bids_tools "${@:3}"
