#!/usr/bin/python
from NDimInv.plot_helper import *
import numpy as np

input_data = np.loadtxt('data/data.dat')

data = {}
tmp = np.loadtxt('results_no_time/stats_and_rms/rho0_results.dat')
data['no-time'] = tmp

tmp = np.loadtxt('results/stats_and_rms/rho0_results.dat')
data['time'] = tmp

tmp = np.loadtxt('results_tw/stats_and_rms/rho0_results.dat')
data['time-tw'] = tmp

times = np.loadtxt('results_no_time/times.dat')

fig, ax = plt.subplots(1, 1)

msizes = [10, 5, 3]
ax.scatter(times, np.log10(input_data[:, 0]), s=70, color='k')
for nr, key in enumerate(data.keys()):
    pass
    ax.plot(times, data[key], '.-', label=key, markersize=msizes[nr])

ax.legend(loc='lower left')

fig.savefig('rho0_comparison.png')
