#!/usr/bin/python
"""

"""
from NDimInv.plot_helper import *
import numpy as np
import os
import lib_cc.main as CC


def generate_data():
    """
    Generate data sets from two Cole-Cole terms
    """
    # set frequencies
    frequencies = np.logspace(-3, 3, 25)

    # generate four sets of Cole-Cole parameters
    rho0 = 50  # Ohm m
    m_list = (0.05, 0.15)
    tau_list = ((40, 0.004),  # both peaks resolved
                (400, 0.0001),  # no peak resolved
                (40, 0.0001),  # low frequency peak resolved
                (400, 0.004)  # high frequency peak resolved
                )
    c = 0.6

    cc_sets = []
    cc_sets.append((np.log(100), 0.05, np.log(0.04), 0.6))
    for tau_set in tau_list:
        cc_pars = [np.log(rho0), ]
        for m, tau in zip(m_list, tau_set):
            cc_pars += [m, np.log(tau), c]
        cc_sets.append(cc_pars)
    print cc_sets

    # generate spectra
    cc = CC.cole_cole()
    settings = {'frequencies': frequencies}
    cc.set_settings(settings)

    rmags = []
    rphas = []
    for nr, cc_set in enumerate(cc_sets):
        rmag, rpha = cc.forward(cc_set)
        rmags.append(np.exp(rmag))
        rphas.append(rpha)
        # debug plot
       #fig, axes = plt.subplots(2, 1)
       #ax = axes[0]
       #ax.semilogx(frequencies, rmag, '.-')

       #ax = axes[1]
       #ax.semilogx(frequencies, -rpha, '.-')

       #fig.savefig('spec_{0:02}.png'.format(nr))
    data = np.hstack((rmags, rphas))
    if(not os.path.isdir('data')):
        os.makedirs('data')
    filename = 'data/data.dat'
    np.savetxt(filename, data)

    np.savetxt('data/frequencies.dat', frequencies)

if __name__ == '__main__':
    generate_data()
