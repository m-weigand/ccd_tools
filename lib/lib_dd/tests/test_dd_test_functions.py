#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests for the dd_test_function module

Run with

nosetests test_dd_test_function.py -s -v

To run a specific test:

nosetests -s -v test_dd_test_function.py:test_dd_test_function

"""
from nose.tools import *
import lib_dd.test_functions as dd_test


class test_dd_test_function():
    @classmethod
    def teardown(self):
        pass

    def setup(self):
        pass

    def _apply_single_t_rms_pos_change(self, old_rms, new_rms,
                                       thresholds, expected_results):
        changes = dd_test.single_t_rms_pos_change(old_rms, new_rms, thresholds)
        print changes
        for change, expected in zip(changes, expected_results):
            assert_equal(change, expected)

    def test_single_t_rms_pos_change(self):
        # set up some old and new rms values
        old_rms = [1.0, 0.5, 0.3]
        new_rms = [1.05, 0.5, 0.2]
        expected_results = [False, True, True]

        for thresholds in (1, [1], [1, ]):
            self._apply_single_t_rms_pos_change(old_rms, new_rms,
                                                thresholds, expected_results)
