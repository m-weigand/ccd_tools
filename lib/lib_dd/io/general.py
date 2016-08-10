import numpy as np
import ascii
import ascii_audit


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


def save_f(fid, final_iterations, norm_factors):
    """write model response directly in a file handler

    Also save forward response format to f_format.dat
    """
    for index, itd in enumerate(final_iterations):
        M = itd[0].Model.convert_to_M(itd[0].m)
        f_data = itd[0].Model.F(M)
        # we know that the first two dimensions belong to frequencies,
        # re/im
        base_dim = f_data.shape[0] * f_data.shape[1]

        if len(f_data.shape) == 3:
            extra_dim = f_data.shape[2]
        else:
            extra_dim = 1
        f_data = f_data.T

        # import pdb
        # pdb.set_trace()
        f_data = f_data.reshape(extra_dim, base_dim)
        if norm_factors is not None:
            print('normalising')
            f_data /= norm_factors[index]
        np.savetxt(fid, f_data)

    open('f_format.dat', 'w').write(itd[0].Data.obj.data_format)
