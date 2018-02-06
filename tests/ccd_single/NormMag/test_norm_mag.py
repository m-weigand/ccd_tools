#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Run with

nosetests test_dd_data.py -s -v
"""
import sys
sys.path.append('..')
from nose.tools import *
import os
import subprocess
import shutil
import numpy as np
import pandas as pd

from sip_models.res.cc import cc
import sip_formats.convert as sip_converter
from collections import namedtuple

cc_pars = namedtuple('ccpars', ('rho0', 'm', 'tau', 'c'))
initial_cc_pars = cc_pars(
    rho0=100,
    m=0.1,
    tau=0.04,
    c=0.6
)


def generate_data(directory, settings):
    """Create data.dat, frequencies.dat in directory using the settings dict

    settings : {'data_format': cre_cim|cmag_cpha|rmag_rpha|rre_rmim,
                'rho0': float,
                'frequencies': np.array()
                }
    """
    cc_obj = cc(settings['frequencies'])

    pars = [initial_cc_pars.rho0,
            initial_cc_pars.m,
            initial_cc_pars.tau,
            initial_cc_pars.c]
    response = cc_obj.response(pars)

    response_converted = sip_converter.convert(
        'rmag_rpha',
        settings['data_format'],
        response.rmag_rpha
    ).flatten(order='F')

    if not os.path.isdir(directory):
        os.makedirs(directory)

    np.savetxt(directory + os.sep + 'frequencies.dat', settings['frequencies'])
    np.savetxt(directory + os.sep + 'data.dat', np.atleast_2d(
        response_converted))


def generate_dd(directory, settings):
    """Create a run_dd.sh batch file using the DD settings stored in the
    settings dict:

    settings : {'Nd': int,
                'lam': float,
                'data_format': sting,
                'model': res|cond,
                }
    """
    batchfile = directory + os.sep + 'run_dd.sh'
    with open(batchfile, 'w') as fid:
        fid.write('#!/bin/bash\n')
        if settings['model'] == 'cond':
            fid.write('DD_COND=1 ')
        fid.write(' DD_STARTING_MODEL=3 ')
        fid.write('ccd_single -c 1')
        fid.write(' -n {0}'.format(settings['Nd']))
        fid.write(' --lambda {0}'.format(settings['lam']))
        if settings['norm'] is not None:
            fid.write(' --norm {0}'.format(settings['norm']))
        fid.write(' --data_format "{0}"'.format(settings['data_format']))
        fid.write(' -o "results" ')
        fid.write('\n')


def _check_io_datafiles(directory, dd_dir, format_orig):
    datafile_orig = directory + '/data.dat'
    datafile_fit = dd_dir + '/data.dat'
    dataformatfile_fit = dd_dir + '/data_format.dat'

    data_orig = np.loadtxt(datafile_orig)
    data_fit = np.loadtxt(datafile_fit)
    dataformat_fit = open(dataformatfile_fit, 'r').readline().strip()

    data_diff = np.abs(data_orig - data_fit)
    assert_equal(dataformat_fit, format_orig)
    assert_greater(1e-5, data_diff.max())
    if data_diff.max() > 1e-5:
        print('Input/output data not equal')
    else:
        print('Input/output data equal')

    if dataformat_fit == format_orig:
        print('data_format checks out')
    else:
        print('data_format is wrong!', dataformat_fit, format_orig)


def _check_rho0(directory, dd_dir, settings_dd):
    intparfile = dd_dir + os.sep + 'integrated_parameters.dat'
    intpars = pd.read_csv(intparfile, sep=' ', skiprows=3)

    rho0_diff = np.abs(
        initial_cc_pars.rho0 - 10 ** intpars['rho0'].values[0]
    ) / initial_cc_pars.rho0
    print('rho0 orig', initial_cc_pars.rho0)
    print('rho0 recovered', 10 ** intpars['rho0'].values[0])
    print('rho0_diff (relative, percentage)', rho0_diff * 1e2)

    if settings_dd['norm'] is None:
        # we expect a discrepancy if no norm is used
        assert_true(rho0_diff > 0.02)
    else:
        # we only allow for 2 percent variation
        assert_true(rho0_diff < 0.02)


def apply_checks(directory, settings_data, settings_dd):
    """Check a given directory for correct results
    """
    dd_dir = directory + os.sep + 'results'

    # _check_io_datafiles(directory, dd_dir, settings_data['data_format'])
    _check_rho0(directory, dd_dir, settings_dd)
    # TODO: more checks


def run_batch(directory):
    pwd = os.getcwd()
    os.chdir(directory)
    p = subprocess.Popen('bash run_dd.sh', shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    os.chdir(pwd)


def case(model, norm, lam, data_format):
    directory = 'case_model_{0}_norm_{1}_format_{2}'.format(model, norm,
                                          data_format)
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    settings_data = {'data_format': data_format,
                     'rho0': 100,
                     'frequencies': np.logspace(-3, 3, 20)
                     }
    generate_data(directory, settings_data)

    settings_dd = {'Nd': 20,
                   'lam': lam,
                   'data_format': data_format,
                   'model': model,
                   'norm': norm
                   }
    generate_dd(directory, settings_dd)
    run_batch(directory)
    apply_checks(directory, settings_data, settings_dd)


def test_generator():
    """Generate the various test cases
    """
    # for model in ('res', 'cond'):
    for model in ('cond', ):
        for norm, lam in zip(
                (None, 0.1, 1, 10),
                (10, 1, 10, 10)
        ):
            for data_format in (
                    'rmag_rpha',
                    'rre_rmim',
                    'cmag_cpha',
                    'cre_cim',
            ):
                def fn(x, y, z, a):
                    case(x, y, z, a)
                fn.description =\
                    'model: {0} norm: {1} data_format {2}'.format(
                        model, norm, data_format)
                yield fn, model, norm, lam, data_format


if __name__ == '__main__':
    test_generator()
