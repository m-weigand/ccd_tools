#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Execute to run single Cole-Cole term characterization
"""
from NDimInv.plot_helper import *
mpl.rcParams['font.size'] = 8.0
import sys
sys.path.append('..')
from nose.tools import *
import subprocess
import os
import numpy as np
import NDimInv.colecole as colecole
import glob
import shutil
shutil

frequencies = np.logspace(-2, 4, 20)


class cls_settings():
    def __init__(self):
        self.datadir = 'DATA'
        self.vars = ['rho0_variation', 'm_variation',
                     'tau_variation', 'c_variation']
        self.Nd = 20

        self.check_and_create_dirs()

    def check_and_create_dirs(self):
        """
        Create missing variation dirs
        """
        if(not os.path.isdir(self.datadir)):
            os.makedirs(self.datadir)

        for item in self.vars:
            dirname = self.datadir + os.sep + item
            if(not os.path.isdir(dirname)):
                os.makedirs(dirname)

settings = cls_settings()


def find_next_free_set(directory):
    """
    Find the next free number of a new set directory with the format:
    set%.3i
    """
    itemlist = sorted(glob.glob(directory + '/set*'))
    next_nr = 1
    for item in itemlist:
        if(os.path.isdir(item)):
            item = os.path.basename(item)
            item_nr = int(item[3:])
            print('item_nr ', item_nr)
            next_nr = item_nr + 1

    setdir = directory + os.sep + 'set{0:03}'.format(next_nr)

    while(os.path.isdir(setdir)):
        next_nr += 1
        setdir = directory + os.sep + 'set{0:03}'.format(next_nr)

    return setdir


def generate_spectra(colecole_parameters, variations, frequencies):
    """
    Generate different Cole-Cole parameter sets (and spectra)
    """
    # find None
    index = np.where(np.isnan(colecole_parameters))[0]
    output_dir = settings.datadir + os.sep + settings.vars[index]

    # generate setdir
    setdir = find_next_free_set(output_dir)
    os.makedirs(setdir)

    fin = np.hstack((frequencies, frequencies))

    # generate Cole-Cole parameters
    cc_sets = np.zeros((len(variations), 4))
    data = []
    for nr, value in enumerate(variations):
        cc_sets[nr, :] = colecole_parameters
        cc_sets[nr, index] = value

        # generate CR response
        magpha = colecole.cole_log(fin, cc_sets[nr])
        magpha[0, :] = np.exp(magpha[0, :])
        data.append(magpha.flatten())

    data = np.array(data)

    # save files
    np.savetxt(setdir + os.sep + 'colecole.pars', cc_sets)
    np.savetxt(setdir + os.sep + 'frequencies.dat', frequencies)
    np.savetxt(setdir + os.sep + 'data.dat', data)


def get_test_cases():
    """
    Find all set directories in the datadir.
    A set directory is characterized by a data.dat and a frequency.dat
    file.
    """
    test_cases = []
    # find all directories with data.dat and frequencies.dat
    # all directories with a command.dat are result directories of the DD
    for root, dirs, files in os.walk(settings.datadir):
        if('data.dat' in files and 'frequencies.dat' in files and
                'command.dat' not in files):
            test_cases.append((root, 'data.dat', 'frequencies.dat'))

    return test_cases


def run_cases(test_cases):
    """
    Run the Debye Decomposition in all test cases.
    """
    for datfreq in test_cases:
        #        yield run_case, datfreq[0], datfreq[1], datfreq[2]
        run_case(datfreq[0], datfreq[1], datfreq[2])


def run_case(directory, data_file, frequency_file):
    # for Nd in (2, 4, 6, 10, 16, 20):
    for Nd in (20, ):
        print('Running ', directory)
        pwd = os.getcwd()
        os.chdir(directory)
        output_dir = 'dd_output_Nd_{0}'.format(Nd)
        cmd = 'dd_single.py -o "{0}" --lambda 30 -c 2 -f '.format(output_dir)
        cmd += '"{0}" -d "{1}" -n {2}'.format(frequency_file, data_file,
                                              Nd)
        result = subprocess.call(cmd, shell=True)
        assert_equal(result, 0)
        os.chdir(pwd)


def plot_results_small(test_cases):
    """
    Only plot selected results
    """
    for case in test_cases:
        print case
        # read in original cc parmaters
        cc_orig = np.loadtxt(case[0] + os.sep + 'colecole.pars')
        for outdir in sorted(glob.glob(case[0] + os.sep + 'dd_output*')):
            print outdir
            prefix = outdir + os.sep
            rho0 = np.loadtxt(prefix + 'stats_and_rms/rho0_results.dat')
            mtotn = np.loadtxt(prefix + 'stats_and_rms/m_tot_n_results.dat')
            # mtotn = np.loadtxt(prefix + 'stats_and_rms/m_tot_n_results.dat')
            tau50 = np.loadtxt(prefix + 'stats_and_rms/tau_50_results.dat')
            taumean = np.loadtxt(prefix + 'stats_and_rms/tau_mean_results.dat')
            taua = np.loadtxt(
                prefix + 'stats_and_rms/tau_arithmetic_results.dat')
            taug = np.loadtxt(
                prefix + 'stats_and_rms/tau_geometric_results.dat')

            # rms_values = np.loadtxt(
            # prefix + 'stats_and_rms/rms_no_err_results.dat')

            fig, axes = plt.subplots(1, 6, figsize=(10, 2))

            # rho0_cc vs rho0_dd
            axes[0].plot(np.exp(cc_orig[:, 0]), 10 ** rho0, '.-', alpha=0.8,
                         label='fit')
            axes[0].scatter(np.exp(cc_orig[:, 0]), np.exp(cc_orig[:, 0]),
                            color='gray', alpha=0.7, s=30, label='1-1')
            axes[0].set_xlabel(r'CC $\rho_0~[\Omega m]$')
            axes[0].set_ylabel(r'DD $\rho_0~[\Omega m]$')
            axes[0].get_xaxis().set_major_locator(mpl.ticker.MaxNLocator(5))
            axes[0].get_xaxis().set_major_formatter(
                mpl.ticker.FormatStrFormatter('%.1f'))

            # m_tot_n^DD vs m_tot_n^CC
            mn = cc_orig[:, 1] / np.exp(cc_orig[:, 0])
            axes[1].plot(mn, 10 ** mtotn, '.-', alpha=0.8)
            axes[1].scatter(mn, mn, color='gray',
                            alpha=0.7, s=30)
            axes[1].set_xlabel(r'CC $m / \rho_0$')
            axes[1].set_ylabel(r'DD $m_{tot}^n$')
            axes[1].get_xaxis().set_major_locator(mpl.ticker.MaxNLocator(5))
            axes[1].get_xaxis().set_major_formatter(
                mpl.ticker.FormatStrFormatter('%.3f'))

            axes[2].plot(np.log10(np.exp(cc_orig[:, 2])), taumean, '.-',
                         alpha=0.8)
            axes[2].scatter(np.log10(np.exp(cc_orig[:, 2])),
                            np.log10(np.exp(cc_orig[:, 2])), color='gray',
                            s=30, alpha=0.7)

            axes[2].set_title(r'$\tau_{mean}$')
            axes[2].set_xlabel(r'CC $log_{10}(\tau)$')
            axes[2].set_ylabel(
                r'DD $\left(\frac{\sum_i m_i \cdot log(\tau_i)}' +
                r'{\sum m_i}\right)$')
            axes[2].get_xaxis().set_major_locator(mpl.ticker.MaxNLocator(3))
            axes[2].get_xaxis().set_major_formatter(
                mpl.ticker.FormatStrFormatter('%.2f'))

            axes[3].plot(np.log10(np.exp(cc_orig[:, 2])), tau50, '.-',
                         alpha=0.8)
            axes[3].plot(np.log10(np.exp(cc_orig[:, 2])),
                         np.log10(np.exp(cc_orig[:, 2])), '-', color='gray',
                         alpha=0.7)

            axes[3].set_xlabel(r'CC $log_{10}(\tau)$')
            axes[3].set_ylabel(r'DD $log_{10}(\tau_{50})$')
            axes[3].get_xaxis().set_major_locator(mpl.ticker.MaxNLocator(3))
            axes[3].get_xaxis().set_major_formatter(
                mpl.ticker.FormatStrFormatter('%.2f'))

            for ax, taud, label, title in zip(
                    (axes[4], axes[5]), (taug, taua),
                    (r'DD $log_{10}\left[\left(\prod \tau_i^{m_i}\right)^' +
                     r'{\frac{1}{\sum m_i}}\right]$',
                     r'DD $log_{10}\left(\frac{\sum m_i \cdot \tau_i}' +
                     r'{\sum m_i}\right)$'),
                    (r'geometrical $\tau$', r'arithmetic $\tau$')):
                ax.plot(np.log10(np.exp(cc_orig[:, 2])), taud, '.-',
                        alpha=0.8)
                ax.set_title(title)

                ax.scatter(np.log10(np.exp(cc_orig[:, 2])),
                           np.log10(np.exp(cc_orig[:, 2])), color='gray',
                           s=30, alpha=0.7)
                ax.set_ylabel(label)
                ax.set_xlabel(r'CC $log_{10}(\tau)$')
                ax.get_xaxis().set_major_locator(mpl.ticker.MaxNLocator(3))

            ax = axes[0]
            ax.legend(loc="lower center", ncol=2, bbox_to_anchor=(0, 0, 1, 1),
                      bbox_transform=fig.transFigure)

            for ax in axes.flatten()[2:]:
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                xylim = (np.min((xlim[0], ylim[0])), np.max((xlim[1], ylim[1])))
                ax.set_xlim(xylim)
                ax.set_ylim(xylim)
                ax.set_aspect('equal')

            for ax in list(axes.flatten()):
                labels = ax.get_xticklabels()
                for label in labels:
                    label.set_rotation(30)

            fig.tight_layout()
            fig.subplots_adjust(bottom=0.45, top=0.85)
            outfile = case[0] + os.sep
            dd_dir = os.path.basename(outdir)
            if(len(dd_dir) > 10):
                outfile += dd_dir[10:]

            outfile += '_dd_comparison_small.png'
            fig.savefig(outfile, dpi=350)
            fig.clf()
            plt.close(fig)


def generate_all_spectra():
    # rho0 variation
    generate_spectra([np.nan, 0.1, np.log(0.04), 0.6],
                     np.log([10, 50, 100, 200, 500, 1000, 2000, 5000, 10000]),
                     frequencies)

    # m variation
    generate_spectra([np.log(100), np.nan, np.log10(0.04), 0.6],
                     [0.01, 0.02, 0.05, 0.08, 0.1, 0.15, 0.2], frequencies)

    # tau variation
    generate_spectra([np.log(100), 0.1, np.nan, 0.6],
                     np.log([0.4, 0.3, 0.2, 0.1, 0.08, 0.06, 0.04, 0.02, 0.01,
                             0.008, 0.004]), frequencies)

    # c variation
    generate_spectra([np.log(100), 0.1, np.log10(0.04), np.nan],
                     [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                     frequencies)


if __name__ == '__main__':
    if(os.path.isdir('DATA')):
        shutil.rmtree('DATA')
    generate_all_spectra()
    test_cases = get_test_cases()
    run_cases(test_cases)
    plot_results_small(test_cases)
