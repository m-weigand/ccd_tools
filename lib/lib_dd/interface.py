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


Functions common to the Cole-Cole decomposition implementations ccd_single,
ccd_time.
"""
import sys
import os
import tempfile

import numpy as np

import sip_formats.convert as SC
# ## general helper functions ###


def create_output_dir(options):
    """ Create the output directory
    """
    # store the final output directory
    outdir = options['output_dir']

    if options['use_tmp']:
        # get temporary directory
        tmp_outdir = tempfile.mkdtemp(suffix='ccd_')
        options['output_dir'] = tmp_outdir
    else:
        if(not os.path.isdir(options['output_dir'])):
            os.makedirs(options['output_dir'])

    return outdir, options


def get_command():
    """Return a string with the full command call, including environment
    variables.

    Environment variables are exported in separate lines
    """
    cmd = ''
    # environment variables
    for key in ('DD_COND',
                'DD_STARTING_MODEL',
                'DD_TAU_X',
                'DD_DEBUG_STARTING_PARS',
                'DD_USE_LATEX',
                'DD_C'):
        if key in os.environ:
            cmd += 'export {0}="{1}"\n'.format(key, os.environ[key])

    # executeable command
    cmd += ' '.join(sys.argv)
    return cmd


def aggregate_dicts(iteration_list, dict_name):
    """
    For a given list of NDimInv iterations, aggregate the dictionaries with
    name 'dict_name' (Iteration.dict_name) and return on dict containing the
    values of all iterations as lists.
    """
    global_stat_pars = {}

    keys = getattr(iteration_list[0][0], dict_name).keys()
    # keys = iteration_list[0][0].stat_pars.keys()
    for it, nr in iteration_list:
        adict = getattr(it, dict_name)
        for key in keys:
            value = adict[key]
            # we need lists to aggregate
            if(type(value) is not list):
                value = [value, ]

            if(key not in global_stat_pars):
                global_stat_pars[key] = value
            else:
                global_stat_pars[key] += value
    return global_stat_pars

# ## load functions ###


def _get_frequencies(options):
    # we can filter by id (0-indexed)
    if options['ignore_frequencies'] is not None:
        f_ignore_ids = [int(x) for x in
                        options['ignore_frequencies'].split(',')]
    else:
        f_ignore_ids = []

    if isinstance(options['frequency_file'], np.ndarray):
        frequencies = options['frequency_file']
    else:
        frequencies = np.loadtxt(options['frequency_file'])

    # or we can filter by values
    if options['data_fmin'] is not None:
        f_below_ids = np.where(frequencies < options['data_fmin'])[0]
        f_ignore_ids.extend(f_below_ids.tolist())

    if options['data_fmax'] is not None:
        f_above_ids = np.where(frequencies > options['data_fmax'])[0]
        f_ignore_ids.extend(f_above_ids.tolist())

    # filter frequencies
    if len(f_ignore_ids) > 0:
        # remove duplicates
        f_ignore_ids = list(set(f_ignore_ids))

        # sort
        f_ignore_ids = sorted(f_ignore_ids)

        frequencies = np.delete(frequencies, f_ignore_ids, axis=0)
    else:
        f_ignore_ids = None

    return frequencies, f_ignore_ids


def load_frequencies_and_data(options):
    """
    Load frequencies and data from options.frequency_file and
    options.data_file. Apply certain processing steps such as:

        * frequency filtering
        * magnitude normalization

    Parameters
    ----------
    options: object as created by optparse (e.g. provided by dd_single.py or
             dd_time.py)

    Returns
    -------
    data: data dict
    options: the options object can be changed by this function, e.g. when the
             data type is changed.
    """
    data = {}

    frequencies, f_ignore_ids = _get_frequencies(options)
    data['frequencies'] = frequencies
    # # data ##
    # # load raw data

    if isinstance(options['data_file'], np.ndarray):
        raw_data = np.atleast_2d(options['data_file'])
    else:
        try:
            raw_data = np.atleast_2d(np.loadtxt(options['data_file']))
        except Exception as e:
            print('There was an error loading the data file')
            print(e)
            exit()

    # # filter frequencies
    if f_ignore_ids is not None:
        # split data for easy access
        part1 = raw_data[:, 0:int(raw_data.shape[1] / 2)]
        part2 = raw_data[:, int(raw_data.shape[1] / 2):]
        part1 = np.delete(part1, f_ignore_ids, axis=1)
        part2 = np.delete(part2, f_ignore_ids, axis=1)
        # rebuild raw_data
        raw_data = np.hstack((part1, part2))

    # we always work with the native model data format
    if int(os.environ.get('DD_COND', 0)) == 1:
        target_format = "cre_cim"
    else:
        target_format = "rre_rim"

    raw_data = SC.convert(options['data_format'], target_format, raw_data)
    options['data_format'] = target_format

    # apply normalization if necessary
    # note, because the previous format transformations, the normalisation can
    # directly be applied (it is always given in the model data format)
    if options['norm'] is not None:
        norm_factors = options['norm'] / raw_data[:, 0]
        norm_factors = norm_factors[:, np.newaxis]

        # apply factors
        raw_data *= norm_factors
        data['norm_factors'] = np.atleast_1d(norm_factors[:, 0].squeeze())

    data['raw_format'] = options['data_format']
    data['raw_data'] = raw_data

    return data, options


# ## save functions ###


def save_stat_pars(stat_pars, norm_factors=None):
    """
    Saves to current working directy.
    """
    # get keys of statistical parameters
    keys = stat_pars.keys()

    # save keys (statistics)
    for key in keys:
        raw_values = stat_pars[key]
        # we need to treat some keys different than others before we can save
        # them
        values = prepare_stat_values(raw_values, key, norm_factors)

        filename = '{0}_results.dat'.format(key)
        np.savetxt(filename, np.atleast_1d(values))


def prepare_stat_values(raw_values, key, norm_factors):
    """
    Prepare stat_pars for saving to disc.

    This included renormalization or padding for specific keys.

    Divide the statistical parameter rho0 by norm_factors and multiply m_tot_n
    by them.

    Returns
    -------
    values: NxM array, with N the number of spectra, and M the number of
            parameters

    """
    # pad variable length parameters with nan so that we can save them to disc
    # using np.savetxt
    if(key == 'tau_peaks_all' or key == 'f_peaks_all'):
        # first iteration: get max. nr of peaks
        max_len = max([len(x) for x in raw_values])

        def padwithnans(vector, pad_width, iaxis, kwargs):
            # pad with np.nans
            # we need this function to accomplish that, see documentation
            # of np.pad
            if(pad_width[1] == 0):
                return vector
            vector[-pad_width[1]:] = np.nan
            return vector

        values = np.array([np.pad(i, (0, max_len - i.size), padwithnans) for i
                           in raw_values])
    else:
        values = np.array(raw_values)
        # values = values.squeeze()

    # renormalize all parameters containing rho0
    # Note: When the conductivity model is used, the normalisation factors
    # refer to the data in conductivities, and correspondingly, sigma_0. As we
    # apply the normalisation to a resistivity (rho_0) parameter, we have to
    # invert the normalisations, which manifests as a sign change in the log
    # operations
    if(key == 'rho0' and norm_factors is not None):
        # rho0 is log10
        # renormalize
        if int(os.environ.get('DD_COND', 0)) == 1:
            values += np.log10(norm_factors).squeeze()
        else:
            values -= np.log10(norm_factors).squeeze()

    if(key == 'sigma0' and norm_factors is not None):
        # sigma0 is log10
        # renormalize
        values -= np.log10(norm_factors).squeeze()

    if key == 'sigma_infty' and norm_factors is not None :
        # sigma0 is log10
        # renormalize
        values -= np.log10(norm_factors).squeeze()

    if(key == 'm_tot_n' and norm_factors is not None):
        # renormalize
        if int(os.environ.get('DD_COND', 0)) == 1:
            values -= np.log10(norm_factors).squeeze()
        else:
            values += np.log10(norm_factors).squeeze()

    # make sure values is a list
    values = np.atleast_2d(values.T).T
    return values


def save_rms_values(rms_list, rms_names):
    """
    Save the RMS values to the corresponding filenames
    """
    for key in rms_list.keys():
        # split key
        key_base = key[:-6]
        key_type = key[-6:]
        names = rms_names[key_base]
        rms_all = np.array(rms_list[key]).T
        if len(names) != rms_all.shape[0]:
            names = [
                names[0] + '{0}'.format(x) for x in
                range(0, rms_all.shape[0])
            ]
        for name, rms in zip(names, rms_all):
            filename = name + key_type + '.dat'
            np.savetxt(filename, np.atleast_1d(rms))
