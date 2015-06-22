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
import dd_test

def test_generator():
    test_cases = []
    # find all directories with data.dat and frequencies.dat and test_func.py
    for root, dirs, files in os.walk('.'):
        if('data.dat' in files and 'frequencies.dat' in files and 'test_func.py' in files):
            test_cases.append((os.path.abspath(root),))

    for test_case in test_cases:
        yield run_case, test_case[0]

def run_case(test_case):
    print('Running', test_case)
    pwd = os.getcwd()
    os.chdir(test_case)
    test_dir = dd_test.get_test_dir([], last=True)
    print('TEST_DIR', test_dir)

    # due to some strange issue with the nose-importer we have to read the
    # current directory entry
    if(not '.' in sys.path):
        sys.path.append('.')
    dd_test.run_test(test_dir)
    os.chdir(pwd)
    #assert_equal(result, 0)
