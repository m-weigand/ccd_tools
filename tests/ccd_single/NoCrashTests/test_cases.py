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
        yield run_case_single_core, datfreq[0], datfreq[1]
        yield run_case_duo_core, datfreq[0], datfreq[1]


def run_case_single_core(data_file, frequency_file):
    if(os.path.isdir(output_dir)):
        shutil.rmtree(output_dir)
    cmd = 'dd_single.py --silent --tmp -c 1 -o "{0}"'.format(output_dir)
    cmd += ' -f "{0}" -d "{1}"'.format(frequency_file, data_file)

    # result = subprocess.Popen(cmd, shell=True, stdout=subprocess.Pipe.:w

    result = subprocess.call(cmd, shell=True)
    assert_equal(result, 0)
    # remove output dir
    shutil.rmtree(output_dir)


def run_case_duo_core(data_file, frequency_file):
    if(os.path.isdir(output_dir)):
        shutil.rmtree(output_dir)
    cmd = 'dd_single.py --silent --tmp -c 2 -o "{0}"'.format(output_dir)
    cmd += ' -f "{0}" -d "{1}"'.format(frequency_file, data_file)
    result = subprocess.call(cmd, shell=True)
    assert_equal(result, 0)
    # remove output dir
    shutil.rmtree(output_dir)
