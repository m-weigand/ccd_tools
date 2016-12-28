#!/usr/bin/python
# -*- coding: utf-8 -*-
from crlab_py.mpl import *
mpl.rcParams['font.size'] = 10.0
import numpy as np
import crlab_py.colecole as cc
# import crlab_py.elem as elem
# import crlab_py.tomodir as TD
# import crlab_py.sipdir as SD
# import os
import crlab_py.spectrum as SPECTRUM
spectrum = SPECTRUM.spectrum()


def tau2f(tau):
    return (1 / (2 * np.pi * tau))


def s2f(s):
    return tau2f(10 ** s)


def plot_imp_spectrum(ax):
    f = np.logspace(-2, 4, 40)
    fin = np.hstack((f, f))

    pars = [np.log(100), 0.05, np.log(0.04), 0.6, 0.1, np.log(1e-4), 0.7]
    erg = cc.cole_log(fin, pars)

    magpha = np.hstack((np.exp(erg[0, :]), erg[1, :]))
    cre, cmim = spectrum.convert_rmagpha_to_creim(magpha)

    np.savetxt('data.dat', magpha)
    np.savetxt('frequencies.dat', f)

    ax.semilogx(f, cmim, '.-', color='r')
    ax.set_ylabel(r"$\sigma''$")

    for i, line in enumerate(ax.get_xticklines() + ax.get_yticklines()):
        line.set_visible(False)
    ax.get_yaxis().set_ticks([])
    ax.get_xaxis().set_ticks([])
    ax.set_xlabel('Frequenz [Hz]')

    pmin = min(cmim)
    pmax = max(cmim)

    # now mark the various tau values
    # tau50 = np.loadtxt('dd_fit/stats_and_rms/tau_50_results.dat')
    # f50 = s2f(tau50)
    # p50 = cmim[np.argmin(np.abs(f - f50))]
    # ax.annotate(
    #     'tau50',
    #     xy=(f50, p50),
    #     xycoords='data',
    #     xytext=(f50, pmin),
    #     arrowprops=dict(arrowstyle="->",
    #                     connectionstyle="arc3")
    # )

    # tau_mean
    taum = np.loadtxt('dd_fit/stats_and_rms/tau_mean_results.dat')
    fm = s2f(taum)
    pm = cmim[np.argmin(np.abs(f - fm))]

    # ax.annotate(
    #     r'$\tau_{\text{mean}}$',
    #     xy=(fm, pm),
    #     xycoords='data',
    #     xytext=(fm / 100, pmax * 0.9),
    #     arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
    # )

    # peaks
    # taup = np.loadtxt('dd_fit/stats_and_rms/tau_peaks_all_results.dat')
    # # offsets = [0, 2e-4]
    # offsets = [0, 2e-4]
    # for nr, tp in enumerate(taup):
    #     fp = s2f(tp)
    #     pp = cmim[np.argmin(np.abs(f - fp))]
    #     ax.annotate(
    #         'peak {0}'.format(nr + 1),
    #         xy=(fp, pp),
    #         xycoords='data',
    #         xytext=(fp * 0.9, pmin + offsets[nr]),
    #         arrowprops=dict(arrowstyle="->", connectionstyle="arc3")
        # )


def plot_m_dist(ax):
    ax.set_xlabel('Relaxationszeiten')
    ax.set_ylabel('m')
    s = np.loadtxt('dd_fit/s.dat')
    m = np.loadtxt('dd_fit/stats_and_rms/m_i_results.dat')

    ax.plot(s, m, '-', color='k')
    ax.set_xlim(s.min(), s.max())
    ax.invert_xaxis()
    for i, line in enumerate(ax.get_xticklines() + ax.get_yticklines()):
        line.set_visible(False)
    ax.get_yaxis().set_ticks([])
    ax.get_xaxis().set_ticks([])

    # ax.axhline(y=-2.2, linestyle='dashed', color='k')
    # ax.annotate('mtot', xy=(s[-2], -2.6), xycoords='data')


if __name__ == '__main__':
    fig, axes = plt.subplots(1, 2, figsize=(10 / 2.54, 3 / 2.54))
    plot_imp_spectrum(axes[0])
    plot_m_dist(axes[1])
    fig.tight_layout()

    # fig.patch.set_alpha(0.0)
    # for ax in fig.axes:
    #    ax.patch.set_alpha(0.0)
    fig.savefig('spectrum.png', dpi=775)
