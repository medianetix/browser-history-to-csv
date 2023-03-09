#!/bin/bash

# execute as root, if accessing multiple users
python3 ./places.py -d /home/user1/.mozilla/firefox/zqvfbcc9.default-release -p user1-
python3 ./places.py -d /home/user2/.mozilla/firefox/l4xwhv3z.default-release -p user2-
python3 ./places.py -d /home/user3/.mozilla/firefox/r5rdggfa.default-release -p user3-

# make dir for storage
STORAGE="/home/admin/stats/`date +'%Y-%m-%d'`";
mkdir -p $STORAGE

# copy creates and copied files to storage dir
cp /tmp/*.csv "$STORAGE/"
cp /tmp/*.sqlite "$STORAGE/"

echo "*** all done ***"
