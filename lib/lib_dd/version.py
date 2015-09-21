"""
Copyright 2014,2015 Maximilian Weigand

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import pkg_resources


def _get_version_numbers():
    """Return a string containing the version numbers of geccoinv and
    dd_interface. The string is meant to be human readable.
    """
    try:
        geccoinv_version = pkg_resources.require('geccoinv')[0].version
    except pkg_resources.DistributionNotFound:
        geccoinv_version = pkg_resources.require('dd-tools')[0].version

    try:
        dd_interface_version = pkg_resources.require('dd_interface')[0].version
    except pkg_resources.DistributionNotFound:
        dd_interface_version = pkg_resources.require('dd-tools')[0].version

    versions = ''.join(('geccoinv version: ',
                        geccoinv_version,
                        '\n',
                        'dd_interface version: ',
                        dd_interface_version))
    return versions

