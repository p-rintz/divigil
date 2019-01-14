#  Copyright (c) 2019. Philipp Rintz
#  pylinuxiso is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pylinuxiso is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re

from modules import utils


def regex(url, file_regex):
    data = utils.getpagedata(url)
    rgx = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/.*?/' + file_regex + '"', re.MULTILINE)
    match = rgx.findall(data)
    return match


def cleanuplink(match):
    isolink = re.sub(r'.*https?://', '', str(match[0]))
    isolink = re.sub(r'".*', '', str(isolink))
    return isolink


def link(section, file_regex, curversion):
    if str(curversion) == '0':
        utils.debug(2, 'Initial search for %s' % section, utils.whoami())
        url = 'https://distrowatch.com/index.php?distribution=' + section + '&release=all&month=all&year=all'
    else:
        utils.debug(2, 'Searching for %s' % section, utils.whoami())
        url = 'https://distrowatch.com/'
    match = regex(url, file_regex)
    if match:
        isolink = cleanuplink(match)
        meta, url = utils.linkinfo(isolink)
        filename = utils.file_name(url)
        if meta.get('Content-Type').split(';')[0] == 'text/html':
            print('Download link for %s is an intermediary website.' % filename)
            print('Will retry getting a download link.')
            match = regex(url, file_regex)
            if len(match) == 0:
                print('Failed to get a download link from the intermediary website. Quitting.')
            else:
                isolink = cleanuplink(match)
                return isolink
        else:
            return isolink
