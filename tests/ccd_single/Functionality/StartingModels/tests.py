#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run with

nosetests test_dd_data.py -s -v
"""
import sys
sys.path.append('..')
from nose.tools import *
import subprocess
import os
import shutil

# we use this directory for output files
output_dir = "test_output"


def test_generator():
    test_cases = []
    # find all directories with data.dat and frequencies.dat
    for root, dirs, files in os.walk('.'):
        # ignore output dir
        if(root == './' + output_dir):
            continue
        if('data.dat' in files and 'frequencies.dat' in files):
            test_cases.append((root + os.sep + 'data.dat',
                               root + os.sep + 'frequencies.dat'))

    for datfreq in test_cases:
        # run test for each starting model
        for starting_model in range(1, 4):
            yield run_case_single_core, datfreq[0], datfreq[1], starting_model


def run_case_single_core(data_file, frequency_file, starting_model):
    outdir = output_dir + '_model_{}'.format(starting_model)
    if(os.path.isdir(outdir)):
        shutil.rmtree(outdir)

    # set environment variable
    os.environ['DD_STARTING_MODEL'] = '{0}'.format(starting_model)

    cmd = 'ccd_single --silent --tmp -c 1 --lambda 50 -o "{0}"'.format(
        outdir)
    cmd += ' -f "{0}" -d "{1}"'.format(frequency_file, data_file)

    # result = subprocess.Popen(cmd, shell=True, stdout=subprocess.Pipe.:w

    result = subprocess.call(cmd, shell=True)
    assert_equal(result, 0)
    # remove output dir
    shutil.rmtree(outdir)
