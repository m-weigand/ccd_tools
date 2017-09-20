import lib_dd.io.ascii as ascii
import lib_dd.io.ascii_audit as ascii_audit


def _make_list(obj):
    """make sure the provided object is a list, if not, enclose it in one
    """
    if not isinstance(obj, list):
        return [obj, ]
    else:
        return obj


def save_fit_results(data, NDobj):
    """
    Save results of all DD fits to files

    Parameters
    ----------
    data:
    NDobj: one or more ND objects. This is either a ND object, or list of ND
           objects
    """
    NDlist = _make_list(NDobj)
    output_format = data['options']['output_format']
    if output_format == 'ascii':
        ascii.save_data(data, NDlist)
    elif output_format == 'ascii_audit':
        ascii_audit.save_results(data, NDlist)
    else:
        raise Exception('Output format "{0}" not recognized!'.format(
            output_format))
