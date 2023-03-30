#!/bin/bash
# execute this script as root or with sudo rights!

STORAGE="/home/hthurat/browser-stats/`date +'%Y-%m-%d'`";
mkdir -p $STORAGE

# copy sqlite databases and write csv files
python3 ./history.py -b firefox -d /home/anna/.mozilla/firefox/zqvfbcc9.default-release -p anna-
python3 ./history.py -b chrome -d /home/anna/.config/chromium/Default -p anna-

python3 ./history.py -b firefox -d /home/nico/.mozilla/firefox/l4xwhv3z.default-release -p nico-
python3 ./history.py -b chrome -d /home/nico/.config/chromium/Default -p nico-

python3 ./history.py -b firefox -d /home/dthurat/.mozilla/firefox/r5rdggfa.default-release -p dthurat-
# python3 ./history.py -b chrome -d /home/dthurat/.config/chromium/Default -p dthurat-

python3 ./history.py -b firefox -d /home/hthurat/.mozilla/firefox/wgp4hxlb.default-release -p hthurat-
python3 ./history.py -b chrome -d /home/hthurat/.config/chromium/Default -p hthurat-

# store files in local dir (/tmp is erased on boot)
cp /tmp/anna-* "$STORAGE/"
cp /tmp/nico-* "$STORAGE/"
cp /tmp/dthurat-* "$STORAGE/"
cp /tmp/hthurat-* "$STORAGE/"

chown -R hthurat:hthurat "$STORAGE"

# copy files to NAS
scp -r "$STORAGE" hthurat@192.168.80.35:/share/homes/hthurat/edv/browser-stats/

echo "*** all done ***"
