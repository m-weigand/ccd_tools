#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-wildcard-import,wildcard-import
"""
Cole-Cole decomposition interface for spectral induced polarization data. One
or more spectra can be fitted using a Debye decomposition approach.

Copyright 2014,2015,2016 Maximilian Weigand

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
# from memory_profiler import *
import logging
logging.basicConfig(level=logging.INFO)
import os
import numpy as np
from multiprocessing import Pool
import shutil
from NDimInv.plot_helper import *
import lib_dd.interface as lDDi
import lib_dd.io.io_general as iog
import lib_dd.config.cfg_single as cfg_single
import lib_dd.decomposition.ccd_single as decomp_single


class ccd_single(object):
    """Cole-Cole decomposition object
    """

    def __init__(self, config):
        self.config = config

    def _filter_nan_values(self, frequencies, cr_spectrum):
        """
            Filter nan values along the frequency axis (we always ne part1 and
            part2).

            Return filtered frequencies, cr_spectrum
        """

        # check for NaN values
        nan_indices = np.isnan(cr_spectrum)
        nan_along_freq = np.any(nan_indices, axis=1)
        to_delete = np.where(nan_along_freq)
        frequencies_cropped = np.delete(frequencies, to_delete)
        cr_spectrum_cropped = np.delete(cr_spectrum, to_delete, axis=0)
        return frequencies_cropped, cr_spectrum_cropped

    def _get_fit_datas(self, data):
        """
        Prepare data for fitting. Prepare a set of variables/objects for each
        spectrum. Also filter nan values

        Parameters
        ----------
        data : dict containing the keys 'frequencies', 'cr_data'
        """
        fit_datas = []

        nr_of_spectra = len(data['cr_data'])
        for i in range(0, nr_of_spectra):
            fit_data = {}
            # change file prefix for each spectrum
            # at the moment we need a copy for this
            frequencies_cropped, cr_data = self._filter_nan_values(
                data['frequencies'], data['cr_data'][i])

            fit_data['prep_opts'] = data['prep_opts']
            fit_data['data'] = cr_data
            fit_data['nr'] = i + 1
            fit_data['nr_of_spectra'] = nr_of_spectra
            fit_data['frequencies'] = frequencies_cropped

            # inversion options are changed for each spectrum, so we have to
            # copy it each time
            inv_opts_i = data['inv_opts'].copy()
            inv_opts_i['frequencies'] = frequencies_cropped
            inv_opts_i['global_prefix'] = 'spec_{0:03}_'.format(i)
            if('norm_factors' in data):
                inv_opts_i['norm_factors'] = data['norm_factors'][i]
            else:
                inv_opts_i['norm_factors'] = None

            fit_data['inv_opts'] = inv_opts_i

            fit_datas.append(fit_data)

        return fit_datas

    def fit_data(self, data):
        """This is the central fit function, which prepares the data, fits each
        spectrum, plots (if requested), and then saves the results.
        """
        fit_datas = self._get_fit_datas(data)

        # fit
        if(data['prep_opts']['nr_cores'] == 1):
            print('single processing')
            # single processing
            results = list(map(decomp_single.fit_one_spectrum, fit_datas))
        else:
            # multi processing
            print('multi processing')
            p = Pool(data['prep_opts']['nr_cores'])
            results = p.map(decomp_single.fit_one_spectrum, fit_datas)

        self.results = results
        self.data = data
        # results now contains one or more ND objects
        # iog.save_fit_results(data, results)

    def get_data_dd_single(self, options):
        """
        Load frequencies and data and return a data dict

        Parameters
        ----------

        options: cmd options


        Returns
        -------
        data: dict with entries "raw_data", "cr_data", "options", "inv_opts",
              "prep_opts"
        """
        data, options = lDDi.load_frequencies_and_data(options)

        # we need list of spectra
        size_y = int(data['raw_data'].shape[1] / 2)
        cr_data = [x.reshape((size_y, 2), order='F') for x in data['raw_data']]

        data['cr_data'] = cr_data

        # we distinguish two sets of options:
        # prep_opts : all settings we need to prepare the inversion (i.e. set
        #             regularization objects)
        # inv_opts : options that are directly looped through to the NDimInv
        # object
        prep_opts, inv_opts = options.split_options()

        data['options'] = options
        data['prep_opts'] = prep_opts
        data['inv_opts'] = inv_opts
        return data


# @profile
def main():
    print('Cole-Cole decomposition, no time regularization')

    options = cfg_single.cfg_single()
    options.parse_cmd_arguments()

    ccds_object = ccd_single(options)
    # ccds_object.fit_data()

    options.check_input_files()
    outdir = lDDi.create_output_dir(options)

    # DD_RES_INV.inversion.setup_logger('dd', outdir, options.silent)
    # logger = logging.getLogger('dd.debye decomposition')

    # logger.info('----------------------------------')
    # logger.info('       Debye Decomposition')
    # logger.info('----------------------------------')
    # logger.info('Frequency file: {0}'.format(options.frequency_file))
    # logger.info('Data file: {0}'.format(options.data_file))
    # frequencies, data_list = get_frequencies_and_data(options)
    data = ccds_object.get_data_dd_single(options)

    # fit the data
    ccds_object.fit_data(data)

    # for the fitting process, change to the output_directory
    pwd = os.getcwd()
    os.chdir(outdir)

    iog.save_fit_results(
        ccds_object.data,
        ccds_object.results
    )

    # logger.info('=======================================')
    # logger.info('     Debye Decomposition finished!     ')
    # logger.info('=======================================')

    # go back to initial working directory
    os.chdir(pwd)

    # move temp directory to output directory
    if options['use_tmp']:
        if os.path.isdir(options['output_dir']):
            print('WARNING: Output directory already exists')
            print('The new inversion can be found here:')
            print((options['output_dir'] + os.sep + os.path.basename(outdir)))
        shutil.move(outdir, options['output_dir'])


if __name__ == '__main__':
    main()
