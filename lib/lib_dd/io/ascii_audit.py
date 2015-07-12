import json
import datetime
import numpy as np
import uuid
import lib_dd.interface as lDDi


def _get_header():
    """Return a header string that can be added to each output file
    """
    uuidstr = str(uuid.uuid4())

    datetimestr = datetime.datetime.strftime(
        datetime.datetime.now(), '%Y%m%d_%Hh:%Mm')

    command = lDDi.get_command()

    # assemble header
    header = '\n'.join(('# id:' + uuidstr,
                        '# ' + datetimestr,
                        '# ' + command))
    return header


def save_results(data, NDlist):
    """Save fit results to the current directory
    """
    norm_factors = getattr(data, 'norm_factors', None)
    header = _get_header()
    final_iterations = [(x.iterations[-1], nr) for nr, x in enumerate(NDlist)]

    save_integrated_parameters(final_iterations, data, header)
    save_frequency_data(final_iterations, data, header)
    save_data(data, norm_factors, final_iterations)


def save_data(data, norm_factors, final_iterations):
    # save original data
    with open('data.dat', 'w') as fid:
        fid.write('#' + data['raw_format'] + '\n')

        orig_data = data['raw_data']
        if norm_factors is not None:
            orig_data = orig_data / norm_factors
        np.savetxt(fid, orig_data)

    # save forwardmodel
    with open('f.dat', 'w') as fid:
        fid.write('#' + final_iterations[0][0].Data.obj.data_format + '\n')
        for index, itd in enumerate(final_iterations):
            f_data = itd[0].Model.f(itd[0].m)[np.newaxis, :]
            if norm_factors is not None:
                f_data /= norm_factors[index]


def save_integrated_parameters(final_iterations, data, header):
    stat_pars = lDDi.aggregate_dicts(final_iterations, 'stat_pars')
    # get keys of statistical parameters
    keys = stat_pars.keys()

    norm_factors = getattr(data, 'norm_factors', None)

    # do not save these values here
    black_list = ['m_data', 'm_i', 'covf', 'covm']

    pars_labels = []
    pars_list = []
    # save keys (statistics)
    for key in keys:
        raw_values = stat_pars[key]
        # we need to treat some keys different than others before we can save
        # them
        values = lDDi.prepare_stat_values(raw_values, key, norm_factors)

        if key not in black_list:
            # print key, values, values.shape
            # print values.shape
            for nr, value in enumerate(values.T):
                # print key, value, value.shape
                postfix = ''
                if nr > 0:
                    postfix = '-{0}'.format(nr)
                pars_labels.append(key + postfix)
                pars_list.append(value)
        else:
            # save to its own file
            with open(key + '.dat', 'w') as fid:
                fid.write(header)
                fid.write('#' + key)
                np.savetxt(fid, values)


    all_data = np.vstack(pars_list).T
    with open('integrated_paramaters.dat', 'w') as fid:
        fid.write(header + '\n')
        fid.write('#' + ' '.join(pars_labels) + '\n')
        np.savetxt(fid, all_data, fmt='%.6f')



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

    orig_data = data['raw_data']
    if norm_factors is not None:
        orig_data = orig_data / norm_factors

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
