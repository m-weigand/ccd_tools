import os
import sys
import re
import shutil
import subprocess

# this is the hard-coded subdirectory where tests are stored
all_tests_directory = 'test_results'


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
        if os.path.isdir(directory + os.sep + item):
            result = regex.match(item)
            if(result is not None):
                largest_number = max((largest_number, int(item)))

    if(last is False):
        largest_number += 1
    new_test_dir = '{0:02}'.format(largest_number)
    print('New directory: {0}'.format(new_test_dir))
    return directory + os.sep + new_test_dir


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


def get_cmd(testcfg_file):
    available_binaries = ('ccd_single', 'ccd_time')
    regexes = [re.compile(x) for x in available_binaries]

    # read test.cfg file, fourth line
    with open(testcfg_file, 'r') as fid:
        cmd = []
        add_to_cmd = False
        # find initial call to ccd_single or ccd_time
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


def run_test(test_dir):
    """
    Execute the actual test

    # call cdd with stored parameters
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

    p = subprocess.check_output(
        cmd,
        shell=True,
        stderr=subprocess.STDOUT,
    )

    sys.path.append(os.getcwd())
    # run the test
    import test_func
    test_func.test_regressions(old_result=test_dir, new_result='active_run')
