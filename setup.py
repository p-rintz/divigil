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

from setuptools import setup


setup(
    name='Divigil',
    version='0.1',
    packages=['modules'],
    install_requires=['apscheduler'],
    url='https://github.com/p-rintz/divigil',
    license='GPL3.0',
    author='Philipp Rintz',
    author_email='git@rintz.net',
    description='Download and keep up-to-date on new releases of various distributions'
)
