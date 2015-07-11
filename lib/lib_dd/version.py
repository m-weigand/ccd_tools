import pkg_resources


def _get_version_numbers():
    """Return a string containing the version numbers of geccoinv and
    dd_interface. The string is meant to be human readable.
    """
    versions = ''.join(('geccoinv version: ',
                        pkg_resources.require('geccoinv')[0].version,
                        '\n',
                        'dd_interface version: ',
                        pkg_resources.require('dd_interface')[0].version))
    return versions

