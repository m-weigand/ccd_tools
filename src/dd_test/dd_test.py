#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various test functions for the debye decomposition routines

Copyright 2014,2015 Maximilian Weigand

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import re
import os
from optparse import OptionParser
import subprocess
import shutil
import sys

#
all_tests_directory = 'test_results'

# dict with the available binaries, and the corresponding data files
available_binaries = {
    'dd_single.py': {
        'data_files': {
            '-f': 'frequencies.dat',
            '-d': 'data.dat'
        }
    },
    'dd_time.py': {
        'data_files': {
            '-f': 'frequencies.dat',
            '-d': 'data.dat',
            '--times': 'times.dat'
        }
    }
}


def handle_cmd_options():
    """
    Handle command line options
    """
    parser = OptionParser()
    for full_binary in sorted(available_binaries.keys()):
        binary = full_binary[:-3]
        parser.add_option("--" + binary,
                          action="store_true",
                          dest=binary,
                          help="Create test for " + binary,
                          default=False)

    parser.add_option("--init", action="store_true", dest="init_record",
                      help="Init a new test result directory (default: False)",
                      default=False)
    parser.add_option("--record", action="store_true",
                      help="Record previously initialized test (default: " +
                      "False)", default=False, dest="record")
    parser.add_option("--test", action="store_true",
                      help="Test the current dd implementation vs recorded " +
                      "results (default: False)", dest="test")

    (options, args) = parser.parse_args()

    if options.init_record:
        nr_found = 0
        for full_binary in sorted(available_binaries.keys()):
            value = getattr(options, full_binary[:-3])
            if value:
                nr_found += 1
                # store the binary for later use
                setattr(options, 'binary', full_binary[:-3])
        if nr_found == 0:
            raise Exception(
                'You MUST provide either --dd_single or --dd_time!')
        if nr_found > 1:
            print('You can use one of the binaries!')

    if(len(args) > 1):
        print('Only one additional argument is allowed (test directory)')
        exit()

    return options, args


def get_test_dir_name(directory, last=False):
    """
    Return the name of a test directory format %.2i

    Parameters
    ----------
    directory: directory containing all test directories
    last: Return last existing directory (True) or next free directory (False)
    """

    # get all directories starting with a number
    regex = re.compile('^[0-9][0-9]$')

    largest_number = 0
    for item in os.listdir(directory):
        if(os.path.isdir(directory + os.sep + item)):
            result = regex.match(item)
            if(result is not None):
                largest_number = max((largest_number, int(item)))

    if(last is False):
        largest_number += 1
    new_test_dir = '{0:02}'.format(largest_number)
    print('New directory: {0}'.format(new_test_dir))
    return directory + os.sep + new_test_dir


def write_pc_infos(fid):
    # get git commit and branch
    git_commit = subprocess.check_output('git log -1 | grep commit',
                                         shell=True)
    git_branch = subprocess.check_output('git branch | grep "\*"', shell=True)
    uname = subprocess.check_output('uname -a', shell=True)
    cpu = subprocess.check_output(
        'cat /proc/cpuinfo  | grep "model name" | head -1', shell=True)
    hostname = subprocess.check_output('hostname', shell=True)
    fid.write(git_commit)
    fid.write(git_branch)
    fid.write(uname)
    fid.write(cpu)
    fid.write(hostname)


def _get_data_files_for_binary(options):
    return available_binaries[options.binary + '.py']['data_files'].values()


def initialize_new_test_dir(options):
    """
    Create all necessary directories and files for a new test
    """
    file_list = _get_data_files_for_binary(options)
    file_list += ['test_func.py', ]

    for filename in file_list:
        if not os.path.isfile(filename):
            raise Exception('File not found: {0}'.format(filename))

    if(not os.path.isdir(all_tests_directory)):
        os.makedirs(all_tests_directory)

    # test_dir = get_test_dir_name(all_tests_directory, last=False)
    # os.makedirs(test_dir)

    # write git status and default line
    test_cfg_file = 'test.cfg'
    with open(test_cfg_file, 'w') as fid:
        fid.write('# edit the following line to your needs\n')
        fid.write('# all lines below the initial dd_single.py call\n')
        fid.write('# will be joined to one CMD line\n')
        fid.write('# do not use the -f and -d (and --times) options. ' +
                  'They will be added\n')
        fid.write('# automatically.\n')
        # now write default dd_single.py call
        default_N = 20
        default_nr_cores = 1
        fid.write(options.binary + '.py\n')
        fid.write('-n {0}\n-c {1}\n--silent\n'.format(
            default_N, default_nr_cores))

    # call vim in order to give the user the opportunity to change to dd call
    subprocess.call('vim {0}'.format(test_cfg_file), shell=True)

    print('Test sucessfully initialized. Record a new test by calling:')
    print('dd_test.py --record')


def get_cmd(testcfg_file):
    available_binaries = ('dd_single.py', 'dd_time.py')
    regexes = [re.compile(x) for x in available_binaries]

    # read test.cfg file, fourth line
    with open(testcfg_file, 'r') as fid:
        cmd = []
        add_to_cmd = False
        # find initial call to dd_single or dd_time
        for line in fid.readlines():
            # if the binaries was already found
            if add_to_cmd:
                cmd.append(line.strip())
            # look for the binaries
            if not line.startswith('#'):
                for regex in regexes:
                    if re.search(regex, line) is not None:
                        cmd.append(line.strip())
                        add_to_cmd = True
    return cmd


def record_test(test_dir):
    """
    Run a test
    """
    print('Recording test {0}'.format(test_dir))
    if not os.path.isdir(test_dir):
        os.makedirs(test_dir)

    cmd = get_cmd('test.cfg')
    cmd += [' -f ../../frequencies.dat ',
            ' --data_file ../../data.dat',
            '--output_format ascii',
            ]
    cmd = ' '.join(cmd)
    pwd = os.getcwd()
    os.chdir(test_dir)
    subprocess.call(cmd, shell=True)
    with open('test_infos.dat', 'w') as fid:
        write_pc_infos(fid)
    os.chdir(pwd)


def run_test(test_dir):
    """
    Execute the actual test

    # call dd with stored parameters
    # execute test snippet
    # -> the test snippet should yield errors usable by nosetests...
    """
    print('Run test')
    if(os.path.isdir('active_run')):
        shutil.rmtree('active_run')

    cmd = get_cmd('test.cfg')
    cmd += ['-f frequencies.dat ',
            '--data_file data.dat',
            '-o active_run',
            '--output_format ascii',
            ]
    cmd = ' '.join(cmd)

    # write to bash file for debug purposes
    with open('active_run.sh', 'w') as fid:
        fid.write(cmd)

    # subprocess.call(test_cmd, shell=True, stdin=PIPE)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()

    sys.path.append(os.getcwd())
    # run the test
    import test_func
    test_func.test_regressions(old_result=test_dir, new_result='active_run')


def get_test_dir(args, last=False):
    if(len(args) == 0):
        test_dir = get_test_dir_name(all_tests_directory, last=last)
    else:
        print('Using user defined test directory')
        test_dir = all_tests_directory + os.sep + args[0]
        if not os.path.isdir(test_dir):
            raise Exception(
                'User supplied directory not found: {0}'.format(test_dir))
    return test_dir

if __name__ == '__main__':
    options, args = handle_cmd_options()

    if(options.init_record is True):
        initialize_new_test_dir(options)

    # we use the last test directory if no test dir was give
    if(options.record is True):
        # run checks
        if(not os.path.isfile('test.cfg') or
           not os.path.isdir(all_tests_directory)):
            raise Exception(
                'Test directory not initialised! Use the --init option first.')
        test_dir = get_test_dir(args)
        record_test(test_dir)

    if(options.test is True):
        test_dir = get_test_dir(args, last=True)
        print('Testing ', test_dir)
        run_test(test_dir)
