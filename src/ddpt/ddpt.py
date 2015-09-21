"""
ddpt.py is the post-processing tool for dd_time.py


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

This tool operates on inversion results created by dd_time.py and offers the
following functions:
    -

Planned features:
    - plot (selected) spectra
    - plot (selected) iterations
    - filter spectra based on statistical values
"""
from optparse import OptionParser
import os
import numpy as np
from NDimInv.plot_helper import *
import glob
import ddps


def handle_cmd_options():
    parser = OptionParser()
    parser.add_option("-i", "--dir", type='string', metavar='DIR',
                      help="dd_time result directory default=results",
                      default="results", dest="result_dir")

    parser.add_option("--plot_stats", action="store_true", dest="plot_stats",
                      help="Plot time evoluation of stats (default: False)",
                      default=False)

    parser.add_option("--compare", action="store_true", dest="compare",
                      help="Compare multiple result directory. work with " +
                      "--plot_stats (default: False)", default=False)

    parser.add_option("--peak", dest="pick_peak", type="string",
                      help="Pick a first relaxation time peak in a certain " +
                      "frequency range", default=None)
    parser.add_option("--plot_peaks", action="store_true", dest="plot_peaks",
                      help="only in combination with --peak. Create plots " +
                      "for the selected times (default: False)", default=False)
    parser.add_option('-o', "--output", dest="output", type="string",
                      help="Output file (default: user_peak.dat",
                      default="user_peaks.dat")
    parser.add_option("--times", dest="times", type="string",
                      help="Time indices to use (start with 0)", default=None)

    (options, args) = parser.parse_args()
    return options, args


def _load_data(result_dir):
    if(not os.path.isdir(result_dir)):
        raise IOError('Directory not found!')

    # load data files
    pwd = os.getcwd()
    os.chdir(result_dir + '/stats_and_rms')
    times = np.loadtxt('../times.dat')
    result_files_raw = glob.glob('*.dat')

    result_files_filtered = []
    for filename in result_files_raw:
        if(filename == 'cums_gtau_results.dat'):
            continue
        if(filename == 'm_i_results.dat'):
            continue
        if(filename.startswith('rms_')):
            continue
        result_files_filtered.append(filename)

    data = {}
    for filename in result_files_filtered:
        key = filename[:-4]
        subdata = np.loadtxt(filename)
        if(subdata.size > 0):
            data[key] = subdata
    os.chdir(pwd)
    return data, times


def plot_stats(options):
    """
    Plot statistics vs. time
    """
    data, times = _load_data(options.result_dir)

    # plot files
    outdir = options.result_dir + '/plots_stats'
    if(not os.path.isdir(outdir)):
        os.makedirs(outdir)
    pwd = os.getcwd()
    os.chdir(outdir)
    for key in data.keys():
        print('Plotting {0}'.format(key))
        fig, ax = plt.subplots(1, 1, figsize=(6, 4))
        ax.set_title(key.replace('_', '\_'))
        ax.plot(times, data[key], '.-')
        fig.savefig(key + '.png')
        plt.close(fig)
        del(fig)
    os.chdir(pwd)


def plot_multiple_stats(options, args):
    # load times
    data_list = []
    time_list = []
    result_dirs = []
    for result_dir in args:
        print('Loading results from {0}'.format(result_dir))
        data, time = _load_data(result_dir)
        data_list.append(data)
        time_list.append(time)
        result_dirs.append(result_dir)

    # plot files
    outdir = 'comparison_stats'
    if(not os.path.isdir(outdir)):
        os.makedirs(outdir)
    pwd = os.getcwd()
    os.chdir(outdir)
    for key in data_list[0].keys():
        print('Plotting {0}'.format(key))
        fig, ax = plt.subplots(1, 1, figsize=(6, 4))
        fig.subplots_adjust(bottom=0.2)
        ax.set_title(key.replace('_', '\_'))
        index = 0
        for times, data in zip(time_list, data_list):
            ax.plot(times, data[key], '.-',
                    label=result_dirs[index].replace('_', '\_'))
            index += 1
        ax.set_xlim([min(times) - 1, max(times) + 1])
        ax.set_xlabel('time')
        # legend
        ax.legend(loc="upper center", ncol=3,
                  bbox_to_anchor=(0, 0, 1, 0.15),
                  bbox_transform=fig.transFigure)
        leg = ax.get_legend()
        ltext = leg.get_texts()
        plt.setp(ltext, fontsize='6')

        fig.savefig(key + '.png')
        plt.close(fig)
        del(fig)
    os.chdir(pwd)


def pick_peak(options):
    # size pars: times x parameters
    pars = np.loadtxt(options.result_dir + '/stats_and_rms/m_i_results.dat')
    frequencies = np.loadtxt(options.result_dir + '/frequencies.dat')
    s = np.loadtxt(options.result_dir + '/s.dat')
    import lib_dd.main as DD
    settings = {'Nd': 10, 'frequencies': frequencies, 'tausel': 'data'}
    obj = DD.get('log10rho0log10m', settings)

    # select times
    time_indices = ddps.extract_indices_from_range_str(options.times,
                                                       pars.shape[0])
    # select frequencies

    # we allow :
    # a) open ranges -100 or 100-
    # b) closed range 50-100
    items = options.pick_peak.split('-')

    # # determine min/max frequency as specified by --peak

    # closed range
    start_f = frequencies[0]
    end_f = frequencies[-1]
    # decide if this index is start or end
    if(items[0] == ''):
        # end range
        end_f = float(items[1])
    elif(items[1] == ''):
        start_f = float(items[0])
    else:
        start_f = float(items[0])
        end_f = float(items[1])

    # convert to s limits
    print('Frequency limits', start_f, end_f)
    end_s = np.log10(1 / (2 * np.pi * start_f))
    start_s = np.log10(1 / (2 * np.pi * end_f))

    # find s indices
    start_s_index = np.argmin(np.abs(s - start_s))
    end_s_index = np.argmin(np.abs(s - end_s))

    freq_slice = slice(start_s_index, end_s_index)
    s_filtered = s[freq_slice]

    f_peak_list = []
    s_peak_list = []
    for time_index in time_indices:
        print ('Time', time_index)
        # apply frequency filter
        pars_filtered = pars[time_index, freq_slice]

        par_time = np.hstack((1, pars_filtered))
        pars_lin = obj.convert_pars_back(par_time)
        # get peak
        s_peaks, tau_peaks, f_peaks = obj.get_peaks(pars_lin[1:], s_filtered)
        f_peak_list.append(f_peaks)
        s_peak_list.append(s_peaks)

    for nr, x in enumerate(f_peak_list):
        if(x.size == 0):
            f_peak_list[nr] = np.nan
            s_peak_list[nr] = np.nan

    pwd = os.getcwd()
    if(not os.path.isdir(options.output)):
        os.makedirs(options.output)
    os.chdir(options.output)

    if(options.plot_peaks):
        # create plots of the rel. times
        nr_plots = len(time_indices)
        size_x = 5
        size_y = 2 * nr_plots
        fig, axes = plt.subplots(nr_plots, 1, figsize=(size_x, size_y))
        for nr, ax in enumerate(axes):
            # ax.plot(s_filtered, pars[time_indices[nr], freq_slice], '.-')
            ax.plot(s, pars[time_indices[nr], :], '.-')
            ax.axvline(x=s_peak_list[nr], color='k')
            ax.set_title('Time: {0}'.format(time_indices[nr]))
            ax.invert_xaxis()
        fig.tight_layout()
        fig.savefig('picked_taus.png', dpi=150)
        plt.close(fig)
        del(fig)

    np.savetxt('peaks.dat', f_peak_list)
    np.savetxt('times.dat', time_indices)
    os.chdir(pwd)


if __name__ == '__main__':
    options, args = handle_cmd_options()

    # call one or more processing steps
    if(options.plot_stats and not options.compare):
        plot_stats(options)

    if(options.plot_stats and options.compare):
        plot_multiple_stats(options, args)

    if(options.pick_peak):
        pick_peak(options)
