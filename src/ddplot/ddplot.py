#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ddplot.py can create plots from plot results created using dd_single.py and
dd_time.py

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
# from memory_profiler import *
import json
from multiprocessing import Pool
import shutil
from optparse import OptionParser
import os
import glob
import numpy as np
from NDimInv.plot_helper import *
import NDimInv.elem as elem
import dd_single
import NDimInv
import lib_dd.plot as lDDp
import sip_formats.convert as SC


def handle_cmd_options():
    parser = OptionParser()
    parser.add_option("-i", "--dir", type='string', metavar='DIR',
                      help="dd_single/dd_time result directory default " +
                      "results",
                      default="results", dest="result_dir")
    parser.add_option("--range", dest="spec_ranges", type="string",
                      help="Pixel range(s) to plot. Separate by ';' and " +
                      "start with 1. For example: \"1;2;4;5\". " +
                      "Also allowed are ranges: \"2-10\", and open ranges: " +
                      "\"5-\" (default: -1 (all))",
                      default=None)
    # parser.add_option("--nr_cpus", type='int', metavar='NR',
    #                   help="Output directory", default=1,
    #                   dest="nr_cpus")
    parser.add_option('-o', "--output", type='str', metavar='DIR',
                      help="Output directory (default: filtered_results)",
                      default='filtered_results',
                      dest="output_dir")

    (options, args) = parser.parse_args()
    return options, args


def _get_result_type(directory):
    """Use heuristics to determine the type of result dir that we deal with

    Possible types are 'ascii' and 'ascii_audit'
    """
    if not os.path.isdir(directory):
        raise Exception('Directory does not exist: {0}'.format(directory))

    if os.path.isdir(directory + os.sep + 'stats_and_rms'):
        return 'ascii'
    else:
        return 'ascii_audit'


def load_ascii_audit_data(directory):
    """We need:

    * frequencies
    * data (rmag_rpha, cre_cim)
    * forward response (rmag_rpha, cre_cim)
    * RTD

    """
    data = {}
    frequencies = np.loadtxt(directory + os.sep + 'frequencies.dat')
    data['frequencies'] = frequencies

    with open(directory + os.sep + 'data.dat', 'r') as fid:
        [fid.readline() for x in range(0, 3)]
        header = fid.readline().strip()
        index = header.find('format:')
        data_format = header[index + 8:].strip()
        subdata = np.loadtxt(fid)
        temp = SC.convert(data_format, 'rmag_rpha', subdata)
        rmag, rpha = SC.split_data(temp)
        data['d_rmag'] = rmag
        data['d_rpha'] = rpha
        temp = SC.convert(data_format, 'cre_cim', subdata)
        rmag, rpha = SC.split_data(temp)
        data['d_cre'] = rmag
        data['d_cim'] = rpha
        temp = SC.convert(data_format, 'rre_rim', subdata)
        rmag, rpha = SC.split_data(temp)
        data['d_rre'] = rmag
        data['d_rim'] = rpha

    with open(directory + os.sep + 'f.dat', 'r') as fid:
        [fid.readline() for x in range(0, 3)]
        header = fid.readline().strip()
        index = header.find('format:')
        data_format = header[index + 8:].strip()
        subdata = np.loadtxt(fid)
        temp = SC.convert(data_format, 'rmag_rpha', subdata)
        rmag, rpha = SC.split_data(temp)
        data['f_rmag'] = rmag
        data['f_rpha'] = rpha
        temp = SC.convert(data_format, 'cre_cim', subdata)
        rmag, rpha = SC.split_data(temp)
        data['f_cre'] = rmag
        data['f_cim'] = rpha
        temp = SC.convert(data_format, 'rre_rim', subdata)
        rmag, rpha = SC.split_data(temp)
        data['f_rre'] = rmag
        data['f_rim'] = rpha

    data['rtd'] = np.atleast_2d(
        np.loadtxt(directory + os.sep + 'm_i.dat', skiprows=4))

    data['tau'] = np.loadtxt(directory + os.sep + 'tau.dat', skiprows=4)

    return data


def load_ascii_data(directory):
    data = {}
    frequencies = np.loadtxt(directory + os.sep + 'frequencies.dat')
    data['frequencies'] = frequencies

    data_format = open(
        directory + os.sep + 'data_format.dat', 'r').readline().strip()

    subdata = np.loadtxt(directory + os.sep + 'data.dat')
    temp = SC.convert(data_format, 'rmag_rpha', subdata)
    rmag, rpha = SC.split_data(temp)
    data['d_rmag'] = rmag
    data['d_rpha'] = rpha
    temp = SC.convert(data_format, 'cre_cim', subdata)
    rmag, rpha = SC.split_data(temp)
    data['d_cre'] = rmag
    data['d_cim'] = rpha
    temp = SC.convert(data_format, 'rre_rim', subdata)
    rmag, rpha = SC.split_data(temp)
    data['d_rre'] = rmag
    data['d_rim'] = rpha


    f_format = open(
        directory + os.sep + 'f_format.dat', 'r').readline().strip()
    subdata = np.loadtxt(directory + os.sep + 'f.dat')
    temp = SC.convert(f_format, 'rmag_rpha', subdata)
    rmag, rpha = SC.split_data(temp)
    data['f_rmag'] = rmag
    data['f_rpha'] = rpha
    temp = SC.convert(f_format, 'cre_cim', subdata)
    rmag, rpha = SC.split_data(temp)
    data['f_cre'] = rmag
    data['f_cim'] = rpha
    temp = SC.convert(f_format, 'rre_rim', subdata)
    rmag, rpha = SC.split_data(temp)
    data['f_rre'] = rmag
    data['f_rim'] = rpha

    data['rtd'] = np.atleast_2d(
        np.loadtxt(directory + os.sep + 'stats_and_rms' + os.sep +
                   'm_i_results.dat'))

    data['tau'] = np.loadtxt(directory + os.sep + 'tau.dat')
    return data


def extract_indices_from_range_str(filter_string, max_index=None):
    """
    Extract indices (e.g. for spectra or pixels) from a range string. The
    string must have the following format: Separate different ranges by ';',
    first index is 1.

    If max_index is provided, open ranges are allowed, as well as "-1" for all.

    Examples:
        "1;2;4;5"
        "2-10"
        "5-"
        "-1"

    Parameters
    ----------
    filter_string : string to be parsed according to the format specifications
    ¦   ¦   ¦   ¦   above
    max_index : (default: None). Provide the maximum index for the ranges to
    ¦   ¦   ¦   allow open ranges and "-1" for all indices
    """
    if(filter_string is None):
        return None

    sections = filter_string.split(';')

    filter_ids = []
    # now look for ranges and expand if necessary
    for section in sections:
        filter_range = section.split('-')
        if(len(filter_range) == 2):
            start = filter_range[0]
            end = filter_range[1]
            # check for an open range, e.g. 4-
            if(end == ''):
                if(max_index is not None):
                    end = max_index
                else:
                    continue
            filter_ids += list(range(int(start) - 1, int(end)))
        else:
            filter_ids.append(int(section) - 1)
    return filter_ids


def plot_data(data, options):
    nr_specs = data['d_rmag'].shape[0]
    indices = extract_indices_from_range_str(options.spec_ranges,
                                             nr_specs)
    if indices is None:
        indices = list(range(0, nr_specs))

    frequencies = data['frequencies']

    for index in indices:
        fig, axes = plt.subplots(1, 5, figsize=(14, 3))

        # Magnitude and phase values
        ax = axes[0]
        ax.semilogx(frequencies, data['d_rmag'][index, :], '.', color='k')
        ax.semilogx(frequencies, data['f_rmag'][index, :], '-', color='k')
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel(r'$|\rho|~[\Omega m]$')
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))
        ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))

        ax = axes[1]
        ax.semilogx(frequencies, -data['d_rpha'][index, :], '.', color='k')
        ax.semilogx(frequencies, -data['f_rpha'][index, :], '-', color='k')
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel(r'$-\phi~[mrad]$')
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))
        ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
        # self._mark_tau_parameters_f(nr, ax, it)

        ## real and imaginary parts
        ax = axes[2]
        ax.semilogx(frequencies, data['d_rre'][index, :], '.', color='k')
        ax.semilogx(frequencies, data['f_rre'][index, :], '-', color='k')
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel(r"$-\rho'~[\Omega m]$", color='k')
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))

        ax = axes[2].twinx()
        ax.semilogx(frequencies, data['d_cre'][index, :], '.', color='gray')
        ax.semilogx(frequencies, data['f_cre'][index, :], '-', color='gray')
        ax.set_ylabel(r"$-\sigma'~[S/m]$", color='gray')
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))

        ax = axes[3]
        ax.semilogx(frequencies, -data['d_rim'][index, :], '.', color='k',
                    label='data')
        ax.semilogx(frequencies, -data['f_rim'][index, :], '-', color='k',
                    label='fit')
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel(r"$-\rho''~[\Omega m]$", color='k')
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))

        ax = axes[3].twinx()
        ax.semilogx(frequencies, data['d_cim'][index, :], '.', color='gray',
                    label='data')
        ax.semilogx(frequencies, data['f_cim'][index, :], '-', color='gray',
                    label='fit')
        # ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel(r"$-\sigma''~[S/m]$", color='gray')
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))

        # self._plot_rtd(nr, axes[nr, 4], M[m], it)

        ax = axes[4]
        ax.semilogx(data['tau'], data['rtd'][index, :], '.-', color='k')
        ax.set_xlabel(r'$\tau~[s]$')
        ax.set_ylabel(r'$log_{10}(m)$')
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))

        fig.tight_layout()
        fig.savefig('spec_{0:03}.png'.format(index), dpi=300)


def _plot_rtd(self, nr, ax, m, it):
    ax.semilogx(it.Data.obj.tau, m[1:], '.-', color='k')
    ax.set_xlim(it.Data.obj.tau.min(), it.Data.obj.tau.max())
    ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=5))
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
    self._mark_tau_parameters_tau(nr, ax, it)
    ax.invert_xaxis()
    # mark limits of data frequencies, converted into the tau space
    tau_min = np.min(it.Model.obj.tau)
    tau_max = np.max(it.Model.obj.tau)
    d_fmin = np.min(it.Data.obj.frequencies)
    d_fmax = np.max(it.Data.obj.frequencies)
    t_fmin = 1 / (2 * np.pi * d_fmin)
    t_fmax = 1 / (2 * np.pi * d_fmax)
    ax.axvline(t_fmin, c='y', alpha=0.7)
    ax.axvline(t_fmax, c='y', alpha=0.7)
    ax.axvspan(tau_min, t_fmax, hatch='/', color='gray', alpha=0.5)
    ax.axvspan(t_fmin, tau_max, hatch='/', color='gray', alpha=0.5,
               label='area outside data range')

    ax.set_xlabel(r'$\tau~[s]$')
    ax.set_ylabel(r'$log_{10}(m)$')

    # print lambda value in title
    title_string = r'$\lambda:$ '
    for lam in it.lams:
        if(type(lam) == list):
            lam = lam[0]
        if(isinstance(lam, float) or isinstance(lam, int)):
            title_string += '{0} '.format(lam)
        else:
            # individual lambdas
            title_string += '{0} '.format(
                lam[m_indices[nr],  m_indices[nr]])
    ax.set_title(title_string)



def _plot_cre_cim(self, nr, axes, orig_data, fit_data, it):
    cre_cim_orig = sip_convert.convert(it.Data.obj.data_format,
                                       'cre_cim',
                                       orig_data)

    cre_cim_fit = sip_convert.convert(it.Data.obj.data_format,
                                      'cre_cim',
                                      fit_data)
    frequencies = it.Data.obj.frequencies
    ax = axes[0]
    ax.semilogx(frequencies, cre_cim_orig[:, 0], '.', color='gray')
    ax.semilogx(frequencies, cre_cim_fit[:, 0], '-', color='gray')
    # ax.set_xlabel('frequency [Hz]')
    ax.set_ylabel(r"$-\sigma'~[S/m]$", color='gray')
    ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))

    ax = axes[1]
    ax.semilogx(frequencies, cre_cim_orig[:, 1], '.', color='gray',
                label='data')
    ax.semilogx(frequencies, cre_cim_fit[:, 1], '-', color='gray',
                label='fit')
    # ax.set_xlabel('frequency [Hz]')
    ax.set_ylabel(r"$-\sigma''~[S/m]$", color='gray')
    ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))

def _plot_rre_rim(self, nr, axes, orig_data, fit_data, it):
    rre_rim_orig = sip_convert.convert(it.Data.obj.data_format,
                                       'rre_rim',
                                       orig_data)

    rre_rim_fit = sip_convert.convert(it.Data.obj.data_format,
                                      'rre_rim',
                                      fit_data)
    frequencies = it.Data.obj.frequencies
    ax = axes[0]
    ax.semilogx(frequencies, rre_rim_orig[:, 0], '.', color='k')
    ax.semilogx(frequencies, rre_rim_fit[:, 0], '-', color='k')
    ax.set_xlabel('frequency [Hz]')
    ax.set_ylabel(r"$-\rho'~[\Omega m]$")
    ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))

    ax = axes[1]
    ax.semilogx(frequencies, -rre_rim_orig[:, 1], '.', color='k',
                label='data')
    ax.semilogx(frequencies, -rre_rim_fit[:, 1], '-', color='k',
                label='fit')
    ax.set_xlabel('frequency [Hz]')
    ax.set_ylabel(r"$-\rho''~[\Omega m]$")
    ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))

    self._mark_tau_parameters_f(nr, ax, it)

    # legend is created from first plot
    if nr == 0:
        ax.legend(loc="upper center", ncol=5,
                  bbox_to_anchor=(0, 0, 1, 1),
                  bbox_transform=ax.get_figure().transFigure)
        leg = ax.get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize='6')

def _mark_tau_parameters_tau(self, nr, ax, it):
    # mark relaxation time parameters
    # mark tau_peak
    for index in range(1, 3):
        try:
            tpeak = it.stat_pars['tau_peak{0}'.format(index)][nr]
            if(not np.isnan(tpeak)):
                ax.axvline(x=10**tpeak, color='k', label=r'$\tau_{peak}^' +
                           '{0}'.format(index) + '$',
                           linestyle='dashed')
        except:
            pass

    try:
        ax.axvline(x=10**it.stat_pars['tau_50'][nr], color='g',
                   label=r'$\tau_{50}$')
    except:
        pass

    try:
        ax.axvline(x=10**it.stat_pars['tau_mean'][nr], color='c',
                   label=r'$\tau_{mean}$')
    except:
        pass

def _mark_tau_parameters_f(self, nr, ax, it):
    # mark relaxation time parameters
    # mark tau_peak
    for index in range(1, 3):
        try:
            fpeak = it.stat_pars['f_peak{0}'.format(index)][nr]
            if(not np.isnan(fpeak)):
                ax.axvline(x=fpeak, color='k', label=r'$\tau_{peak}^' +
                           '{0}'.format(index) + '$',
                           linestyle='dashed')
        except:
            pass

    try:
        ax.axvline(x=it.stat_pars['f_50'][nr], color='g',
                   label=r'$\tau_{50}$')
    except:
        pass

    try:
        ax.axvline(x=it.stat_pars['f_mean'][nr], color='c',
                   label=r'$\tau_{mean}$')
    except:
        pass


def load_data(options):
    result_type = _get_result_type(options.result_dir)
    loading_funcs =  {'ascii': load_ascii_data,
                      'ascii_audit': load_ascii_audit_data
                      }
    data = loading_funcs[result_type](options.result_dir)
    return data


if __name__ == '__main__':
    options, _ = handle_cmd_options()
    data = load_data(options)
    plot_data(data, options)
