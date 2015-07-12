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
        dd_interfaces_version = pkg_resources.require('dd_interfaces')[0].version
    except pkg_resources.DistributionNotFound:
        dd_interfaces_version = pkg_resources.require('dd-tools')[0].version

    versions = ''.join(('geccoinv version: ',
                        geccoinv_version,
                        '\n',
                        'dd_interface version: ',
                        dd_interfaces_version))
    return versions

