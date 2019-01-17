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


import re

from modules import utils

chkurl = 'https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/MD5SUMS'


def chksum(filename, path):
    filepath = path + filename
    checksum = utils.getpagedata(chkurl).split(' ', 1)[0]
    chkresult = utils.chkcalc(checksum, filepath)
    return chkresult


def regex(url, file_regex):
    data = utils.getpagedata(url)
    rgx = re.compile(file_regex, re.MULTILINE)
    match = rgx.findall(data)
    return match


def combinelink(match, url):
    isolink = url + match[0]
    return isolink


def link(section, file_regex, curversion):
    url = 'https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/'
    utils.debug(2, 'Searching for %s' % section, utils.whoami())
    match = regex(url, file_regex)
    if match:
        isolink = combinelink(match, url)
        meta, isolink = utils.linkinfo(isolink)
        return isolink
