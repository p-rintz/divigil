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
import time

import getopt
import importlib
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from modules import download, utils


def printhelp(exitlevel):
    print("%s: [-h]elp [-d]ebug= [-c]onfig=" % sys.argv[0])
    sys.exit(exitlevel)


def timecalc(denom, interv):
    if denom == 'seconds':
        return interv
    elif denom == 'minutes':
        intervalsec = interv * 60
        return intervalsec
    elif denom == 'hours':
        intervalsec = interv * 3600
        return intervalsec
    elif intdenom == 'days':
        intervalsec = interv * 86400
        return intervalsec
    else:
        raise ValueError('Wrong interval denomination.')


def tick():
    print('Tick! The time is: %s' % datetime.now())


def mainloop():
    utils.debug(2, '-----mainloop(start)-----', utils.whoami())
    for i in dllist:
        curversion = str(utils.config.get(i, 'current_version'))
        downloadcfg = str(utils.config.get(i, 'download'))
        file_regex = str(utils.config.get(i, 'file_regex'))
        linkprovider = str(utils.config.get(i, 'link_provider'))
        chkresult = ''
        if str(downloadcfg) == '1':
            try:
                create = importlib.import_module(linkprovider)
                dllink = create.link(i, file_regex, curversion)
            except ModuleNotFoundError:
                print('No link provider %s found.' % linkprovider)
                print('Please check your config again.')
                sys.exit(2)
            except Exception as e:
                print('There was an exception in the %s module.' % linkprovider)
                print(e)
                sys.exit(2)
            if dllink:
                utils.debug(2, 'Download link is %s' % dllink, utils.whoami())
                file_name = utils.file_name(dllink)
                utils.debug(2, 'Filename is %s' % file_name, utils.whoami())
                if file_name == curversion:
                    utils.debug(1, 'We already have the current version for %s.' % i, utils.whoami())
                else:
                        dlinfo = download.download(dllink, dlpath)
                        if hasattr(create, 'chkurl'):
                            utils.debug(3, 'Starting checksum check for %s' % linkprovider, utils.whoami())
                            chkresult = create.chksum(file_name, dlpath)
                        # utils.linkinfo may return an Exception with HTTP Error code. Dont update current_version then.
                        if not utils.is_number(dlinfo) and chkresult is not 'Fail':
                            utils.config.set(i, 'current_version', file_name)
                            utils.debug(2, 'Current_version is: ' + utils.config.get(i, 'current_version'), utils.whoami())
                            with open(utils.configfile, 'w') as configfile:
                                utils.config.write(configfile)
                        elif utils.is_number(dlinfo):
                            print('Download failed with HTTP error code: %s' % dlinfo)
                        else:
                            print('Download failed due to checksum mismatch.')
            else:
                utils.debug(4, 'No download link found for %s' % i, utils.whoami())
        else:
            utils.debug(2, 'Download for %s is set to off.' % i, utils.whoami())
    utils.debug(2, '-----mainloop(stop)-----', utils.whoami())


def main(dlist, path, dbglevel):
    print("Starting up. Reading Config.")
    utils.debug(1, 'Config is: %s' % utils.configfile, utils.whoami())
    if len(path) == 0:
        raise ValueError('You must specify a path in the %s configfile.' % utils.configfile)
    utils.debug(1, 'Download folder is: ' + path, utils.whoami())
    utils.debug(1, 'Downloads in config are:', utils.whoami())
    utils.debug(1, '\n'.join(dlist) + '\n', utils.whoami())
    intervalsec = timecalc(intdenom, interval)
    utils.debug(3, 'Interval is %s seconds' % intervalsec, utils.whoami())
    mainloop()
    if not dbglevel >= 5:
        startscheduler(intervalsec, dbglevel)
    else:
        print('')
        print('----- We are running in one-off mode. (debuglevel >= 5) -----')


def startscheduler(intervalsec, dbglevel):
    scheduler = BackgroundScheduler()
    if dbglevel >= 4:
        scheduler.add_job(tick, 'interval', seconds=10)
    scheduler.add_job(mainloop, 'interval', seconds=intervalsec)
    scheduler.start()
    print()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()


if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules'))
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:c:h', ['debug=', 'config=', 'help'])
        debuglevel = ''
    except getopt.error:
        printhelp(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printhelp(0)
        elif opt in ("-c", "--config"):
            utils.configfile = arg
        elif opt in ("-d", "--debug"):
            debuglevel = int(arg)
    if len(utils.configfile) < 10:
        print("Something's missing in the Configfile")
        printhelp(2)
    dllist, dlpath, interval, intdenom, debuglevel = utils.readconfig(utils.configfile, debuglevel)
    utils.debug(4, (str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules'))), 'mainscript')
    utils.debug(4, ('Path is:' + str(sys.path)), 'mainscript')
    main(dllist, dlpath, debuglevel)
