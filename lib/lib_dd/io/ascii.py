"""save results as ASCII files to a given directory

This is the default output format
"""
import os
import json

import numpy as np

import lib_dd.version as version
import lib_dd.interface as lDDi
import lib_dd.io.helper as helper


def save_base_results(final_iterations, data):
    """
    Save data files that are shared between
    dd_single.py/dd_time.py/dd_space_time.py
    """
    # convert all arrays to lists
    for key in data['inv_opts'].keys():
        if isinstance(data['inv_opts'][key], np.ndarray):
            data['inv_opts'][key] = data['inv_opts'][key].tolist()
    with open('inversion_options.json', 'w') as fid:
        json.dump(data['inv_opts'], fid)

    with open('version.dat', 'w') as fid:
        fid.write(version._get_version_numbers() + '\n')

    # with open('data_format.dat', 'w') as fid:
    #     fid.write(final_iterations[0][0].Data.obj.data_format + '\n')

    # save call to debye_decomposition.py
    with open('command.dat', 'w') as fid:
        cmd = lDDi.get_command()
        fid.write(cmd)

    final_iterations[0][0].RMS.save_rms_definition('rms_definition.json')

    # save tau/s
    np.savetxt('tau.dat', final_iterations[0][0].Data.obj.tau)
    np.savetxt('s.dat', final_iterations[0][0].Data.obj.s)

    # save frequencies/omega
    np.savetxt('frequencies.dat', final_iterations[0][0].Data.obj.frequencies)
    np.savetxt('omega.dat', final_iterations[0][0].Data.obj.omega)

    # save weighting factors
    Wd_diag = final_iterations[0][0].Data.Wd.diagonal()
    np.savetxt('errors.dat', Wd_diag)

    # save lambdas
    # TODO: We want all lambdas, not only from the last iteration
    try:
        lambdas = [x[0].lams for x in final_iterations]
        np.savetxt('lambdas.dat', lambdas)
    except Exception as e:
        print('There was an error saving the lambda values')
        print(e)
        pass

    # save number of iterations
    nr_of_iterations = [x[0].nr for x in final_iterations]
    np.savetxt('nr_iterations.dat', nr_of_iterations, fmt='%i')

    # save normalization factors
    if('norm_factors' in data):
        np.savetxt('normalization_factors.dat', data['norm_factors'])


def save_data(data, NDlist):
    """Save fit results to the current directory
    """
    final_iterations = [(x.iterations[-1], nr) for nr, x in enumerate(NDlist)]

    save_base_results(final_iterations, data)
    if not os.path.isdir('stats_and_rms'):
        os.makedirs('stats_and_rms')
    os.chdir('stats_and_rms')
    stats_for_all_its = lDDi.aggregate_dicts(final_iterations, 'stat_pars')
    if('norm_factors' in data):
        norm_factors = data['norm_factors']
    else:
        norm_factors = None
    lDDi.save_stat_pars(stats_for_all_its, norm_factors)

    rms_for_all_its = lDDi.aggregate_dicts(final_iterations, 'rms_values')
    lDDi.save_rms_values(rms_for_all_its, final_iterations[0][0].RMS.rms_names)
    os.chdir('..')

    # save original data
    with open('data.dat', 'wb') as fid:
        orig_data = data['raw_data']
        if norm_factors is not None:
            orig_data = orig_data / norm_factors[:, np.newaxis]
        np.savetxt(fid, orig_data)

    # (re)save the data format
    # open('data_format.dat', 'w').write(prep_opts['data_format'])
    open('data_format.dat', 'w').write(data['raw_format'])

    # save model response
    with open('f.dat', 'wb') as fid:
        helper.save_f(fid, final_iterations, norm_factors)

    # save times
    if 'times' in data:
        np.savetxt('times.dat', data['times'])
