import csv
import sys
import argparse
import urllib2
from datetime import datetime
import re
import math

def downloadData(url):
    f = urllib2.urlopen(url)
    return f

def processing(data):
    d = csv.reader(data, delimiter=',',dialect=csv.excel_tab)
    browser_types   = [0, 0, 0, 0]
    b_type_name     = ["Chrome", "Safari", "Internet Explorer", "Firefox"]
    hour_hits       = zip(tuple(range(0,24)), (0,0)*12)
    c = 0
    for i, index in enumerate(d,start=0):
        path    = index[0]
        dt      = index[1]
        browser = index[2]
        stat    = index[3]
        size    = index[4]

        if re.search(".png$|.jpg$|.gif$", path): c += 1

        chrome  = re.search("Chrome/[0-9][0-9].[0-9].[0-9][0-9][0-9][0-9].[0-9]", browser)
        safari  = re.search("Version/[0-9].[0-9].[0-9] Safari/|Version/[0-9].[0-9] Mobile/10A5355d Safari/", browser)
        ie      = re.search("MSIE [0-9][0-9]|MSIE [0-9].[0-9]|MSIE [0-9][0-9].[0-9]", browser)
        firefox = re.search("Firefox/[0-9][0-9].[0-9]", browser)

        if chrome:  browser_types[0] = browser_types[0] + 1
        if safari:  browser_types[1] = browser_types[1] + 1
        if ie:      browser_types[2] = browser_types[2] + 1
        if firefox: browser_types[3] = browser_types[3] + 1

        curr_hour = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S').time().hour
        hour_hits[curr_hour] = list(hour_hits[curr_hour])
        hour_hits[curr_hour][1] += 1
        hour_hits[curr_hour] = tuple(hour_hits[curr_hour])

    percent = (float(c)/float(i+1))*100
    most_popular_browser = max(browser_types)
    print(hour_hits)
    print("Image requests account for " + str(round(percent, 2)) + "% of all requests.")
    print(b_type_name[browser_types.index(most_popular_browser)] + ' is the most popular browser with ' + str(most_popular_browser) + ' hits.')

    for t in hour_hits:
        print("Hour " + str(t[0]) + " had " + str(t[1]) + " hits")

def init():
    if len(sys.argv) <= 2:
        exit()
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='Enter a valid URL')
    arg = parser.parse_args()
    data = downloadData(arg.url)
    processing(data)

init()
