"""
    store history for Firefox or Chrome 
    as CSV file in a temporary directory
"""

from argparse import ArgumentParser
import sys
import os
import shutil
import sqlite3
import csv


def write_csvfile(csv_filename, rows):

    # write csv file 
    with open(csv_filename, 'w') as fh:
        writer = csv.writer(fh, delimiter='\t', lineterminator='\n')
        writer.writerows(rows)


def chrome_history(cursor, filename):

    print("- Chrome -")
    # chrome timestamp starts 1601-01-01, so we have to substract 11644473600 secs to get unixepoch !
    cursor.execute("""
    SELECT
        u.id,
        u.url,
        SUBSTR(SUBSTR(j.url, INSTR(j.url, '//') + 2), 0, INSTR(SUBSTR(j.url, INSTR(j.url, '//') + 2), '/')) AS host,
        u.visit_count,
        u.last_visit_time,
        DATETIME(ROUND(u.last_visit_time / 1000000-11644473600), 'unixepoch', 'localtime') AS last_access 
    FROM 
        urls AS u
    LEFT JOIN 
        urls AS j
    ON 
        u.id=j.id
    ORDER BY 
        host, u.id ASC;
    """)
    rows = cursor.fetchall()
    write_csvfile(filename, rows)


def firefox_history(cursor, filename):

    print("- Firefox -")
    # firefix timestamp starts 1970-01-01
    cursor.execute("""
        SELECT 
            p.id, 
            p.url, 
            o.host, 
            p.visit_count, 
            p.last_visit_date AS last_visit_time, 
            datetime(ROUND(p.last_visit_date / 1000000), 'unixepoch', 'localtime') AS last_access 
        FROM 
            moz_places AS p
        LEFT JOIN 
            moz_origins AS o
        ON 
            o.id=p.origin_id
        ORDER BY 
            o.host, p.id ASC;
    """)
    rows = cursor.fetchall()
    write_csvfile(filename, rows)


if __name__ == '__main__':

    parser = ArgumentParser(description="Copy firefox or chrome history file (sqlite) to /tmp folder with prefixed name and create CSV file from it.")
    parser.add_argument("-b", "--browser", dest="browser", default="firefox", choices=['firefox','chrome'], help="browser [firefox|chrome]")
    parser.add_argument("-d", "--dir", dest="filedir", required=True, help="profile directory (firefox-url=about:support), required")
    parser.add_argument("-f", "--filename", dest="filename", default="", help="name of history sqlite db file (firefox=places.sqlite, Chrome=History)")
    parser.add_argument("-p", "--prefix", dest="prefix", default="", help="prefix for the output files (e.g. 01- or myuser-)")
    parser.add_argument("-t", "--tmpdir", dest="tmpdir", default="/tmp", help="temporary dir to store output files (must be writeable, default=/tmp)")
    args = parser.parse_args()

    # get proper filename for database file or use user input
    if args.filename=="":

        if args.browser=='firefox':
            filename = 'places.sqlite'
        elif args.browser=='chrome':
            filename ='History'
        else:
            sys.exit("Unknown browser")

    else:
        # use user input
        filename = args.filename

    # creating file path and copy database file to temp dir with prefix
    orig_dbfile = os.path.join(args.filedir, filename)
    dbfile = os.path.join(args.tmpdir, args.prefix + filename)
    shutil.copy2(orig_dbfile, dbfile)

    # open copied database (due to possible database lock) and create cursor
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    csv_filename = os.path.join(args.tmpdir, args.prefix + args.browser + '-history.csv')

    # query history and build csv file
    if args.browser=="firefox":
        firefox_history(cur, csv_filename)
    else:
        chrome_history(cur, csv_filename)
    
    # be sure to close the connection
    con.close()

    print("*** done ***")
