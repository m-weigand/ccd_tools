#!/usr/bin/env python
""" Create 3D plots for each variation
"""
from NDimInv.plot_helper import *
from mpl_toolkits.mplot3d import Axes3D
Axes3D
import os
import glob
import numpy as np


def read_data(nd_dir):
    """
    Return a dict
    """
    data = {}
    # read in rho0
    data['Nd'] = int(os.path.basename(nd_dir)[13:])
    data['rho0'] = np.loadtxt(nd_dir + '/stats_and_rms/rho0_results.dat')
    data['m_tot_n'] = np.loadtxt(nd_dir + '/stats_and_rms/m_tot_n_results.dat')
    data['tau_peak'] = np.loadtxt(
        nd_dir + '/stats_and_rms/tau_peak1_results.dat')

    return data


def get_nd_data(var_dir):
    set_dir = var_dir + '/set001'
    # get Nd dirs
    expr = os.sep.join((set_dir, 'dd_output*'))
    nd_dirs = sorted(glob.glob(expr))
    nd_data = []
    for nd_dir in nd_dirs:
        print('Reading', nd_dir)
        data = read_data(nd_dir)
        nd_data.append(data)
    return nd_data


def plot_variation(var_dir):
    print('Plotting', var_dir)
    nd_data = get_nd_data(var_dir)
    cc_orig = np.loadtxt(var_dir + '/set001/colecole.pars')
    print(cc_orig)
    print(nd_data)

    fig = plt.figure()
    axes = [fig.add_subplot(2, 2, nr, projection='3d') for nr in range(0, 4)]
#    ax = fig.add_subplot(111, projection='3d')

    for nd in nd_data:
        for nr, key in enumerate(('rho0', 'm_tot_n', 'tau_peak')):
            ax = axes[nr]
            if(key in ('rho0', 'tau_peak')):
                orig = np.exp(cc_orig[:, nr])
                rec = 10 ** nd[key]
            else:
                orig = cc_orig[:, nr]
                rec = nd[key]

            ax.scatter(orig, rec, nd['Nd'])
            ax.plot(orig, orig, '-')

    ax.set_xlabel('CC orig')
    ax.set_ylabel('DD')
    ax.set_zlabel('Nd')
    ax.view_init(110, 100)

    filename = os.path.basename(var_dir)
    filename += '3d.png'
    fig.savefig(filename)
    exit()


if __name__ == '__main__':
    # get variations
    variations = os.listdir('DATA')
    for var_dir in variations:
        plot_variation('DATA/' + var_dir)
        exit()
