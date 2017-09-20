# -*- coding: utf-8 -*-
""" Copyright 2014-2017 Maximilian Weigand

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
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


# some files got renamed during refactoring
# this dict collects the various names for those files
equivalent_rms_files = {
    'both_no_err': ['rms_both_no_err.dat', 'rms_all_noerr.dat'],
    're_no_err': ['rms_part1_no_err.dat', 'rms_real_parts_noerr.dat'],
    'im_no_err': ['rms_part2_no_err.dat', 'rms_imag_parts_noerr.dat'],
    'both_err': ['rms_both_err.dat', 'rms_all_error.dat'],
    're_err': ['rms_part1_err.dat', 'rms_real_parts_error.dat'],
    'im_err': ['rms_part2_err.dat', 'rms_imag_parts_error.dat']
}


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

    """
    rms_files = ('rms_both_err.dat', 'rms_both_no_err.dat', 'rms_part1_err.dat',
                 'rms_part1_no_err.dat', 'rms_part2_err.dat',
                 'rms_part2_no_err.dat')
    """

    for rms_key, rms_files in equivalent_rms_files.items():
        print('Testing key {0}'.format(rms_key))
        base_old = old_result + os.sep + 'results/stats_and_rms/'
        filename_old = [base_old + x for x in rms_files if
                        os.path.isfile(base_old + x)]
        if filename_old:
            rms_old_result = np.atleast_1d(np.loadtxt(filename_old[0]))
        else:
            raise IOError('No RMS file found for old RMS (key {0}) {1}'.format(
                rms_key, base_old))

        base_new = new_result + os.sep + 'stats_and_rms/'
        filename_new = [base_new + x for x in rms_files if
                        os.path.isfile(base_new + x)]
        if filename_new:
            rms_new_result = np.atleast_1d(np.loadtxt(filename_new[0]))
        else:
            raise IOError(
                'No RMS file found for new RMS (key {0}) {1} {2}'.format(
                    rms_key, base_new, os.getcwd()))

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
