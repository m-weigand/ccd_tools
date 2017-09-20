import json
import datetime
import uuid

import numpy as np

import lib_dd.interface as lDDi
import lib_dd.version as version
import lib_dd.io.helper as helper


def _get_header():
    """Return a header string that can be added to each output file
    """
    uuidstr = str(uuid.uuid4())

    datetimestr = datetime.datetime.strftime(
        datetime.datetime.now(), '%Y%m%d_%Hh:%Mm')

    command = lDDi.get_command().split("\n")
    command = ';'.join(command)

    # assemble header
    header = '\n'.join(('# id:' + uuidstr,
                        '# ' + datetimestr,
                        '# ' + command))
    header += '\n'
    return header


def save_results(data, NDlist):
    """Save fit results to the current directory
    """
    norm_factors = data.get('norm_factors', None)
    header = _get_header()
    final_iterations = [(x.iterations[-1], nr) for nr, x in enumerate(NDlist)]

    save_integrated_parameters(final_iterations, data, header)
    save_frequency_data(final_iterations, data, header)
    save_data(data, norm_factors, final_iterations)

    with open('frequencies.dat', 'wb') as fid:
        fid.write(bytes(header, 'UTF-8'))
        fid.write(bytes('# frequencies [Hz]\n', 'UTF-8'))
        np.savetxt(fid, final_iterations[0][0].Data.obj.frequencies)

    with open('tau.dat', 'wb') as fid:
        fid.write(bytes(header, 'UTF-8'))
        fid.write(bytes(
            '# relaxation times used for the decomposition\n',
            'UTF-8')
        )
        np.savetxt(fid, final_iterations[0][0].Data.obj.tau)

    # final_iterations[0][0].RMS.save_rms_definition('rms_definition.json')

    # save lambdas
    # TODO: We want all lambdas, not only from the last iteration
    try:
        lambdas = [x[0].lams[0] for x in final_iterations]
        nr_of_iterations = [x[0].nr for x in final_iterations]
        nr_its_and_lambdas = np.vstack((nr_of_iterations, lambdas)).T

        with open('lams_and_nr_its.dat', 'wb') as fid:
            fid.write(bytes(header, 'UTF-8'))
            fid.write(bytes(
                'nr-its lambda\n',
                'UTF-8'
            ))
            np.savetxt(fid, nr_its_and_lambdas)  # , fmt='%i %f')
    except Exception as e:
        print('There was an error saving the lambda and nr its values')
        print(e)
        pass

    # save normalization factors
    if('norm_factors' in data):
        with open('normalization_factors.dat', 'wb') as fid:
            fid.write(bytes(header, 'UTF-8'))
            fid.write(bytes('# normalisation factors\n', 'UTF-8'))
            np.savetxt(fid, data['norm_factors'])

    # save weighting factors
    Wd_diag = final_iterations[0][0].Data.Wd.diagonal()
    with open('errors.dat', 'wb') as fid:
        fid.write(bytes(header, 'UTF-8'))
        fid.write(
            bytes(
                '# weighting factors, scheme: {0}\n'.format(
                    data['inv_opts']['data_weighting'],
                ),
                'UTF-8'
            )
        )
        np.savetxt(fid, Wd_diag)

    with open('version.dat', 'wb') as fid:
        fid.write(bytes(header, 'UTF-8'))
        fid.write(bytes(
            version._get_version_numbers() + '\n', 'UTF-8')
        )

    iopts = data['inv_opts']
    for key in iopts.keys():
        if isinstance(iopts[key], np.ndarray):
            iopts[key] = iopts[key].tolist()

    with open('inversion_options.json', 'wb') as fid:
        fid.write(bytes(header, 'UTF-8'))
        fid.write(bytes('# inversion options dict\n', 'UTF-8'))
        fid.write(bytes(
            json.dumps(iopts),
            'UTF-8'
        ))


def save_data(data, norm_factors, final_iterations):
    header = _get_header()
    # save original data
    with open('data.dat', 'wb') as fid:
        fid.write(bytes(header, 'UTF-8'))
        out_str = '# raw data, format: ' + data['raw_format'] + '\n'
        fid.write(bytes(out_str, 'UTF-8'))

        orig_data = data['raw_data']
        if norm_factors is not None:
            orig_data = np.atleast_2d(orig_data) / norm_factors[:, np.newaxis]
        np.savetxt(fid, orig_data)

    # save forward response
    with open('f.dat', 'wb') as fid:
        fid.write(bytes(header, 'UTF-8'))
        fid.write(bytes(
            '# forward response data format: ' +
            final_iterations[0][0].Data.obj.data_format + '\n',
            'UTF-8'
        ))
        helper.save_f(fid, final_iterations, norm_factors)

    # save times
    if 'times' in data:
        with open('times.dat', 'wb') as fid:
            fid.write(bytes(header, 'UTF-8'))
            # write column description
            fid.write(bytes(
                '# time of each spectrum\n', 'UTF-8')
            )
            np.savetxt(fid, data['times'])


def save_integrated_parameters(final_iterations, data, header):
    stat_pars = lDDi.aggregate_dicts(final_iterations, 'stat_pars')
    # get keys of statistical parameters
    keys = stat_pars.keys()

    norm_factors = data.get('norm_factors', None)

    # do not save these values here
    black_list = ['m_data', 'm_i', 'covf', 'covm']

    pars_labels = []
    pars_list = []
    # save keys (statistics)
    for key in sorted(keys):
        raw_values = stat_pars[key]
        # we need to treat some keys different than others before we can save
        # them
        values = lDDi.prepare_stat_values(raw_values, key, norm_factors)

        if key not in black_list:
            for nr, value in enumerate(values.T):
                postfix = ''
                if nr > 0:
                    postfix = '-{0}'.format(nr)
                pars_labels.append(key + postfix)
                pars_list.append(value)
        else:
            if key not in ('m_data', ):
                # save to its own file
                with open(key + '.dat', 'wb') as fid:
                    fid.write(bytes(header, 'UTF-8'))
                    out_str = '#' + key + '\n'
                    fid.write(bytes(out_str, 'UTF-8'))
                    np.savetxt(fid, values)

    all_data = np.vstack(pars_list).T
    with open('integrated_parameters.dat', 'wb') as fid:
        fid.write(bytes(header, 'UTF-8'))
        out_str = '#' + ' '.join(pars_labels) + '\n'
        fid.write(bytes(out_str, 'UTF-8'))
        np.savetxt(fid, all_data, fmt='%.6f')


def save_frequency_data(final_iterations, data, header):
    if('norm_factors' in data):
        norm_factors = data['norm_factors']
    else:
        norm_factors = None

    # save frequencies/omega
    # frequencies = final_iterations[0][0].Data.obj.frequencies
    # Wd_diag_1d = final_iterations[0][0].Data.Wd.diagonal()
    # nr_x = int(Wd_diag_1d.size / frequencies.size)

    # Wd_diag_2d = Wd_diag_1d.reshape(frequencies.size, nr_x)

    orig_data = data['raw_data']
    if norm_factors is not None:
        orig_data = np.atleast_2d(orig_data) / norm_factors[:, np.newaxis]

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
