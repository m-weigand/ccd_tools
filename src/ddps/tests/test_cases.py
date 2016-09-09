#!/usr/bin/python
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
import fnmatch


def test_generator():
    test_cases = []
    # find all directories with test.sh
    for root, dirs, files in os.walk('.'):
        results = fnmatch.filter(files, 'test*.sh')
        if(results):
            for filename in results:
                test_cases.append((os.path.abspath(root), filename))

    for test_case in test_cases:
        yield run_case, test_case[0], test_case[1]


def run_case(directory, filename):
    print('Running', directory, filename)
    pwd = os.getcwd()
    os.chdir(directory)
    cmd = './{0}'.format(filename)
    result = subprocess.call(cmd, shell=True)
    # if the command returns 1, then there was an error during the execution
    assert_equal(result, 0)
    print('result', result)
    os.chdir(pwd)
