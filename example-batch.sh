#!/bin/bash
# execute as root, if accessing pathes outside your homedir

# make dir for storage
STORAGE="/home/admin/stats/`date +'%Y-%m-%d'`";
mkdir -p $STORAGE

# user1: firefox and chrome
python3 ./history.py -d /home/user1/.mozilla/firefox/zqvfbcc9.default-release -p user1-
python3 ./history.py -d /home/user1/.config/google-chrome/Default -p user1-

# user2: firefox
python3 ./history.py -d /home/user2/.mozilla/firefox/l4xwhv3z.default-release -p user2-

# user3: chrome
python3 ./history.py -d /home/user3/.config/google-chrome/Default -p user3-

# copy creates and copied files to storage dir
cp /tmp/*.csv "$STORAGE/"
cp /tmp/*.sqlite "$STORAGE/"

echo "*** all done ***"
