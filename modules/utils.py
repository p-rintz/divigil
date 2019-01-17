#!/usr/bin/python3

#  Copyright (c) 2019. Philipp Rintz
#  Divigil is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Divigil is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys

import configparser
import urllib.error
import urllib.request
from pathlib import Path
from re import sub

configdir = str(Path.home()) + '/.config/divigil/'
configfile = configdir + 'config'
config = configparser.ConfigParser()
config.optionxform = str


def readconfig(cfgfile, debugarglevel):
    global debuglevel
    config.read([cfgfile])
    dlpath = config.get('mainconfig', 'folder')
    dllist = config.sections()
    dllist.remove('mainconfig')
    debuglevel = int(config.get('mainconfig', 'debug'))
    interval = int(config.get('mainconfig', 'interval'))
    intdenom = str(config.get('mainconfig', 'interval_denomination'))
    if not is_number(debugarglevel):
        return dllist, dlpath, interval, intdenom, debuglevel
    else:
        debuglevel = debugarglevel
        return dllist, dlpath, interval, intdenom, debugarglevel


def getpagedata(url):
    res = urllib.request.urlopen(url)
    data = res.read()
    data = data.decode("utf-8")
    return data


def linkinfo(url):
    filename = file_name(url)
    if "http" in url:
        url = sub('https?://', '', url)
    try:
        url_https = 'https://' + url
        info = urllib.request.urlopen(url_https)
        url = url_https
    except Exception as e:
        if hasattr(e, 'code'):
            print('HTTP Error %s for: %s ' % (e.code, filename))
            dlinfo = e.code
            return dlinfo
        else:
            print(e.reason, " - Can't connect to https://%s" % url)
            print('Retrying non-ssl connection.')
            try:
                url_http = 'http://' + url
                info = urllib.request.urlopen(url_http)
                url = url_http
            except Exception as e:
                print('Download failed: %s for %s' % (e, filename))
    meta = info.info()
    return meta, url


def debug(debugfunclevel, msg, who):
    if debuglevel >= debugfunclevel:
        print('Debug[' + str(debugfunclevel) + '][' + str(who) + ']: ' + msg)


def chkcalc(chksum, filename):
    import hashlib
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    if hash_md5.hexdigest() == chksum:
        debug(4, 'Checksum checks out.', whoami())
        return 1
    else:
        print('Checksum does not check out.')
        return 0

def is_number(n):
    return str(n).replace('.', '', 1).isdigit()


def whoami():
    return sys._getframe(1).f_code.co_name


def file_name(url):
    if url:
        filename = url.split('/')[-1]
        return filename


#def chksum():
