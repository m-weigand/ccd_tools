#!/usr/bin/python
"""
Analyse the DD for various Nd values
"""
from NDimInv.plot_helper import *
import numpy as np
import glob
import os

dd_dirs_raw = sorted(glob.glob('dd_*'))
# sort into lambdas
dd_dirs = {}
for dd_dir in dd_dirs_raw:
    lam = dd_dir[3:7]
    if(lam in dd_dirs):
        dd_dirs[lam].append(dd_dir)
    else:
        dd_dirs[lam] = [dd_dir, ]

pars = {'tau_50': 'tau_50_results.dat',
        'tau_mean': 'tau_mean_results.dat',
        'tau_peak1': 'tau_peak1_results.dat',
        'm_tot': 'm_tot_results.dat',
        'm_tot_n': 'm_tot_n_results.dat'

        }

labels = {'tau_50': r'$\tau_{50}$',
          'tau_mean': r'$\tau_{mean}$',
          'tau_peak1': r'$\tau_{peak}^1$',
          'm_tot': r'$m_{tot}$',
          'm_tot_n': r'$m_{tot}^n$',
          }

nr_plots = 1 + len(pars.keys())
nr_cols = len(dd_dirs.keys())
size_x = nr_cols * 2.5
size_y = nr_plots * 2
fig, axes = plt.subplots(1 + len(pars.keys()), nr_cols, figsize=(size_x,
                                                                 size_y))

for col, lam_key in enumerate(sorted(dd_dirs.keys())):
    # aggregate data
    data = {}
    data['Nd'] = []
    data['rms_im'] = []

    for key in pars.keys():
        data[key] = []

    for dd in dd_dirs[lam_key]:
        Nd = int(dd[11:])
        # quick check if something went wrong
        if(not os.path.isfile(dd + '/stats_and_rms/rms_part2_no_err.dat')):
            continue
        data['Nd'].append(Nd)

        rms_im = np.loadtxt(dd + '/stats_and_rms/rms_part2_no_err.dat')
        # load pars values
        for key, item in pars.iteritems():
            tmp = np.loadtxt(dd + '/stats_and_rms/{0}'.format(item))
            data[key].append(tmp)
        data['rms_im'].append(float(rms_im))

    # plot data
    ax = axes[0, col]
    ax.plot(data['Nd'], data['rms_im'], '.', color='k')
    ax.set_xlabel('Nd')
    ax.set_ylabel(r'$RMS_{im}$')

    for nr, key in enumerate(pars.keys()):
        ax = axes[nr + 1, col]
        ax.plot(data['Nd'], data[key], '.', color='k')
        ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
        ax.set_xlabel('Nd')
        if key in labels:
            ax.set_ylabel(labels[key])
    axes[0, col].set_title('lambda: {0}'.format(lam_key))

# equalize all limits
for row in range(0, nr_plots):
    # first run: get min/max
    miny = None
    maxy = None
    for col in range(0, nr_cols):
        lims = axes[row, col].get_ylim()
        print 'lims', lims
        miny = min((miny, lims[0]))
        maxy = max((maxy, lims[1]))

    # now set
    for col in range(0, nr_cols):
        axes[row, col].set_ylim((miny, maxy))

fig.tight_layout()
fig.savefig('Nd_comparison.png', dpi=300)
