import json
import datetime
import lib_dd.interface as lDDi

def _get_header():
    """Return a header string that can be added to each output file
    """
    datetimestr = datetime.datetime.strftime(
        datetime.datetime.now(), '%Y%m%d_%Hh:%Mm')

    command = lDDi.get_command()

    # assemble header
    header = '\n'.join(('# ' + datetimestr,
                        '# ' + command))
    return header


def save_data(data, NDlist):
    """Save fit results to the current directory
    """
    header = _get_header()
    print header
    final_iterations = [(x.iterations[-1], nr) for nr, x in enumerate(NDlist)]

    save_frequency_data(final_iterations, data, header)

def save_frequency_data(final_iterations, data, header):
    if('norm_factors' in data):
        norm_factors = data['norm_factors']
    else:
        norm_factors = None

    # save frequencies/omega
    frequencies = final_iterations[0][0].Data.obj.frequencies

    # save weighting factors
    Wd_diag = final_iterations[0][0].Data.Wd.diagonal().reshape(
        (frequencies.size, 2))

    print Wd_diag.shape

    orig_data = data['raw_data']
    if norm_factors is not None:
        orig_data = orig_data / norm_factors
    print orig_data.shape

    # (re)save the data format
    # open('data_format.dat', 'w').write(prep_opts['data_format'])
    # open('data_format.dat', 'w').write(data['raw_format'])

    # save model response
    # with open('f.dat', 'w') as fid:
    #     for index, itd in enumerate(final_iterations):
    #         f_data = itd[0].Model.f(itd[0].m)[np.newaxis, :]
    #         if norm_factors is not None:
    #             f_data /= norm_factors[index]
    #         np.savetxt(fid, f_data)
    # open('f_format.dat', 'w').write(itd[0].Data.obj.data_format)
