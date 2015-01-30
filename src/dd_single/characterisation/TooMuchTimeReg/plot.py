#!/usr/bin/python
from plot_settings import *
import numpy as np
import sip_formats.convert as SC


def plot_specs(ax, result_dir, specs):
    # load data
    f = np.loadtxt(result_dir + '/frequencies.dat')
    response = np.loadtxt(result_dir + '/f.dat')
    data = np.loadtxt(result_dir + '/data.dat')
    data_format = open(result_dir + '/data_format.dat', 'r').readline().strip()

    cre_cim = SC.convert(data_format, 'cre_cim', data)
    cre, cim = SC.split_data(cre_cim)

    fcre_cim = SC.convert(data_format, 'cre_cim', response)
    fcre, fcim = SC.split_data(fcre_cim)

    # plot cmim
    for spec_nr in specs:
        ax.semilogx(f, cim[spec_nr, :] * 1e4, '.', color='gray', label='data')
        ax.semilogx(f, fcim[spec_nr, :] * 1e4, '.-', color='k', label='fit',
                    linewidth=0.5)
        ax.set_ylabel(r"$\sigma''~[\mu S/cm]$")
        ax.set_xlabel('frequency (Hz)')
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=3))
        # ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
        ax.yaxis.set_major_locator(mpl.ticker.FixedLocator([1, 5, 9]))


def plot_rtd(ax, result_dir, rtd_nr, color):
    # load data
    f = np.loadtxt(result_dir + '/frequencies.dat')
    tau_f_min = 1 / (f[-1] * np.pi * 2)
    tau_f_max = 1 / (f[0] * np.pi * 2)
    m_i = np.loadtxt(result_dir + '/stats_and_rms/m_i_results.dat')
    tau = np.loadtxt(result_dir + '/tau.dat')

    ax.semilogx(tau, m_i[rtd_nr, :], '.-', color=color)

    # mark extended tau range
    ax.axvspan(tau[0], tau_f_min, color='gray', hatch='/', alpha=0.5)
    ax.axvspan(tau_f_max, tau[-1], color='gray', hatch='/', alpha=0.5)

    ax.set_xlim((min(tau), max(tau)))
    ax.set_xlabel(r'$\tau~[s]$')
    ax.set_ylabel(r'$log_{10}(\textit{m})$')

    ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=7))
    # ax.xaxis.set_major_locator(mpl.ticker.FixedLocator([1e1, 1e2]))
    # ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
    ax.yaxis.set_major_locator(mpl.ticker.FixedLocator([-5, -3, -1]))
    ax.invert_xaxis()

    # ax.set_title('time {0}'.format(rtd_nr + 1))


def plot_time_evolution(ax, result_dirs):
    # ax2 = ax.twinx()
    colors = ('k', 'gray')
    index = 0
    ax.set_ylabel(r'$\textit{m}_{tot}^n~[mS/m]$')
    for axx, result_dir in zip((ax, ax), result_dirs):
        # plot m_tot_n
        m_tot_n = np.loadtxt(result_dir + '/stats_and_rms/m_tot_n_results.dat')
        print index, colors[index]
        axx.plot(1e3 * 10**m_tot_n, '.-', color=colors[index])
        index += 1
    ax.set_xlabel('time')
    # ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
    ax.yaxis.set_major_locator(mpl.ticker.FixedLocator([0, 1.6, 3.2]))


if __name__ == '__main__':

    fig, axes = plt.subplots(2, 2, figsize=(3.6, 2.25))
    ax = axes[0, 0]
    plot_specs(ax, 'results_good', range(0, 20))

    ax = axes[0, 1]
    plot_time_evolution(ax, ('results_good', 'results_bad_3'))

    ax = axes[1, 0]
    plot_rtd(ax, 'results_good', 9, 'k')

    ax = axes[1, 1]
    plot_rtd(ax, 'results_bad_3', 9, 'gray')

    # set global limits for RTD
    rtd_min = min(min((axes[1, 0].get_ylim(), axes[1, 1].get_ylim())))
    rtd_max = max(max((axes[1, 0].get_ylim(), axes[1, 1].get_ylim())))
    print rtd_min, rtd_max

    rtd_min = -6
    rtd_max = -1
    for ax in axes[1, :].flatten():
        ax.set_ylim((rtd_min, rtd_max))

    ######
    # labels a) - d)
    for nr, ax in enumerate(axes.flatten(order='C')):
        ax.annotate('{0})'.format(chr(97 + nr)), xy=(-0.2, -0.53),
                    xycoords='axes fraction')

    fig.tight_layout()
    fig.savefig('fig7_too_much_time_reg.png', dpi=300)
    # fig.savefig('fig7_too_much_time_reg.pdf', dpi=300)
