#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Invert spatial time-lapse complex resistivity data using the Debye Decoposition
approach.

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

Input files
===========

times : text file, one timestep per line
frequencies : text file, one frequency per line, in ascending order
data_index : index file, one file path per line, corresponding to the times.
data_files : files indexed in *data_index*, holds spatial data for one time
             step, one complex restivity spectrum per line

Plan
====

* jeder Pixel sollte geschrieben werden sobald er fertig gefitted wurde
* abgebrochene Fits sollten weitergeführt werden können
* partielle Ergebnisse sollten wir schon in einer Gitter plottten können
    -> pixel indices
* speichere jede Zeitreihe in einen Unteroder (durch Aufruf der entsprechenden
  dd_time Methoden)
* danach: führe die Ergebnisse zusammen
"""
import os
import numpy as np
import glob
import shutil
import dd_time
import dd_single
import lib_dd.interface as lDDi


def _get_cr_data(options):
    """
    Read in the data index file and the import the complex resistivity spectra
    for all time steps
    """
    # read index
    # the data_index holds relative file paths
    dirname = os.path.dirname(options.data_file)
    if dirname == '':
        dirname = '.'

    with open(options.data_file, 'r') as fid:
        data_index = [dirname + os.sep + x.strip() for x in fid.readlines()]

    # read SIP data
    time_rmag = []
    time_rpha = []
    for data_file in data_index:
        print('Reading timestep data: ', data_file)
        step_data = np.loadtxt(data_file)
        center = step_data.shape[1] / 2
        rmag = step_data[:, 0:center]
        rpha = step_data[:, center:]
        time_rmag.append(rmag)
        time_rpha.append(rpha)

    trmag = np.array(time_rmag)
    trpha = np.array(time_rpha)
    pixel_data = np.concatenate((trmag, trpha), axis=2)

    return pixel_data


def get_data(options):
    """
    Read frequencies and data, and apply frequency filters
    """
    data = {}
    frequencies, f_ignore_ids = lDDi._get_frequencies(options)
    data['frequencies'] = frequencies
    data['times'] = dd_time._get_times(options)

    cr_data = _get_cr_data(options)
    data['sip_data'] = cr_data

    return data


def get_fit_status(outdir, nr_ts):
    """Return the fit status, i.e. how many times series where fitted yet. This
    is determined by the directory with the hightest number in the format
    "tmp_ts_%.Xi", where X is the number of digits of the maximum time series
    number

    Parameters
    ----------
    outdir: output directoy
    nr_ts: number of time series
    """
    nr_digits = int(np.floor(np.log10(nr_ts)) + 1)
    results = sorted(glob.glob(outdir + '/fits/tmp_ts_*'))
    result_dirs = [x for x in results if os.path.isdir(x)]
    if not result_dirs:
        return -1, nr_digits
    else:
        max_result_nr = int(os.path.basename(result_dirs[-1])[-nr_digits:])
    return max_result_nr, nr_digits


def fit_space_time_data(options, outdir):
    """Fit each time series separately by using the corresponding fit function
    from dd_time
    """
    prep_opts, inv_opts = dd_time.split_options(options)
    data = get_data(options)
    max_ts_nr = data['sip_data'].shape[1]
    fit_status, nr_digits = get_fit_status(outdir, nr_ts=max_ts_nr)

    # for the fitting process, change to the output_directory
    pwd = os.getcwd()
    os.chdir(outdir)
    if not os.path.isdir('fits'):
        os.makedirs('fits')
    os.chdir('fits')
    pwd_outdir = os.getcwd()
    for ts_nr in xrange(fit_status, max_ts_nr):
        print('Fitting time series {0}/{1}'.format(ts_nr + 1, max_ts_nr))
        # fit in temp directory
        temp_dir = 'tmp_fit'
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        os.chdir(temp_dir)
        data['cr_data'] = data['sip_data'][:, ts_nr, :].squeeze()
        dd_time.fit_sip_data(data, prep_opts, inv_opts)
        # fit_data(data, prep_opts, inv_opts)
        # go back to initial working directory
        os.chdir(pwd_outdir)
        ts_dir = r'tmp_ts_{0:0' + '{0}'.format(nr_digits) + '}'
        ts_dir = ts_dir.format(ts_nr)
        shutil.move(temp_dir, ts_dir)
    os.chdir(pwd)

if __name__ == '__main__':
    options = dd_time.handle_cmd_options()
    outdir = dd_single.get_output_dir(options)
    fit_space_time_data(options, outdir)
