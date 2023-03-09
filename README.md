# browser-history-to-csv
Creates CSV files for Firefox and Chrome browser history (tested under Linux, may work under Windows as well)

Usage:
- Copy the history.py file to your home directory (e.g. /home/user)
- open terminal
- Type: `python history.py -h` to read the help

Params:
- -d / --dir = directory where the history db (sqlite file) is located (e.g: /home/jdoe/.config/google-chrome/Default). Firefox user enter "about:support" as url and find the information under "Profile directory" (e.g.: /home/jdoe/.mozilla/firefox/ho66093f.default-release)
- -b / --browser = Which browser to use (firefox|chrome)
- -f / --filename = filename for sqlite file (optional, if standard files (firefox = places.sqlite, chrome = History))
- -p / --prefix = prefix for output files in temporary directory, default='', consider using a trailing dash for readability ('jdoe-')
- -t / --tmpdir = directory to write output files and copy the sqlite files (all with given prefix), default='/tmp'

Example usage:
- Chrome, user jdoe `python history.py -d /home/jdoe/.config/google-chrome/Default -b chrome`

