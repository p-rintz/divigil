#!/usr/bin/python3

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

import urllib.error
import urllib.request

from modules import utils


def download(url, path):
        meta, url = utils.linkinfo(url)
        filename = utils.file_name(url)
        try:
            file_size = int(meta.get('Content-Length'))
            file_size = ((file_size / 1024) / 1024) / 1024
            print("Downloading %s with size %s GB" % (filename, file_size))
        except Exception as e:
            print("It was exception type: %s" % e)
            print("Downloading %s" % filename)
        urllib.request.urlretrieve(url, path + filename)
        utils.debug(1, "Download for %s finished" % filename, utils.whoami())
