import os
import numpy as np
from nose.tools import *


class tcolors:
    # see http://ascii-table.com/ansi-escape-sequences.php
    HEADER = '\033[95m'
    OKBLUE = '\033]94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    GRAY = '\033[37m'


def t_rms_pos_change(old_result, new_result, allowed_percentage):
    """
    Test for positive rms changes

    Parameters
    ----------
    old_result: dd directory containing the old run
    new_rusult: dd directory containing the new run
    allowed_percentage: percentage threshold for positive changes.
                        If this variable is a list of length three the
                        values will be treated as rms, rms_re, rms_im
                        thresholds

    """
    rms_files = ('rms_both_err.dat', 'rms_both_no_err.dat', 'rms_part1_err.dat',
                 'rms_part1_no_err.dat', 'rms_part2_err.dat',
                 'rms_part2_no_err.dat')

    for rms_file in rms_files:
        print('Testing {0}'.format(rms_file))
        filename_old = old_result + os.sep + 'results/stats_and_rms/'
        filename_old += os.sep + rms_file
        rms_old_result = np.atleast_1d(np.loadtxt(filename_old))

        filename_new = new_result + os.sep + '/stats_and_rms/' + rms_file
        rms_new_result = np.atleast_1d(np.loadtxt(filename_new))

        for spec_id in range(0, rms_old_result.size):
            print('Spectrum {0}'.format(spec_id + 1))
            assert_single_t_rms_pos_change(rms_old_result[spec_id],
                                           rms_new_result[spec_id],
                                           allowed_percentage)


def single_t_rms_pos_change(rms_old_result, rms_new_result,
                            allowed_percentage):
    """
    Process one spectrum as described in the documentation of t_rms_pos_change

    Parameters
    ----------
    rms_old_result : list/array with 3 entries containing the RMS-values from
                     the last recorded dd fit: Overall RMS, Real part RMS,
                     Imaginary part RMS
    rms_new_result : list/array with 3 entries containing the RMS-values from
                     the test  dd fit: Overall RMS, Real part RMS,
                     Imaginary part RMS
    allowed_percentage : one percentage value for the allowed change
                         between old and new result.

    Returns
    -------
    rms_within_limit : list with 3 bool entries; True for values within the
                       allow percentage change, False for a larger deviation
    """
    rms_change = (rms_new_result - rms_old_result) / rms_old_result * 100
    # a positive change always indicates that rms_new was smaller than old
    line_color = None
    if(rms_change > 0 and rms_change > allowed_percentage):
        line_color = (tcolors.FAIL)
        change = False
    elif(rms_change < 0):
        line_color = (tcolors.OKGREEN)
        change = True
    else:
        line_color = (tcolors.GRAY)
        change = True

    print('{0} percentage change: {1:.5} % (from {2} to {3}) {4}\n'
          .format(line_color, rms_change, rms_old_result,
                  rms_new_result, tcolors.ENDC))
    return change


def assert_single_t_rms_pos_change(rms_old_result, rms_new_result,
                                   allowed_percentage):
    """
    Wrap assertTrue statements around the function
    """
    change = single_t_rms_pos_change(rms_old_result, rms_new_result,
                                     allowed_percentage)
    # raise errors for too large values
    assert_true(change, True)
