"""Copyright 2014-2017 Maximilian Weigand

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
    sip_models_version = pkg_resources.require('sip_models')[0].version
    geccoinv_version = pkg_resources.require('geccoinv')[0].version
    ccd_tools_version = pkg_resources.require('ccd_tools')[0].version

    versions = ''.join((
        'sip_models version: ', sip_models_version, '\n',
        'geccoinv version: ', geccoinv_version, '\n',
        'ccd_tools version: ', ccd_tools_version, '\n'
    ))
    return versions
