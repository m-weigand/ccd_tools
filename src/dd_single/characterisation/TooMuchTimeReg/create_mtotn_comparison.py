#!/usr/bin/python
from NDimInv.plot_helper import *
import numpy as np

#input_data = np.loadtxt('data/data.dat')

data = {}
tmp = np.loadtxt('results_no_time/stats_and_rms/m_tot_n_results.dat')
data['no-time'] = tmp

tmp = np.loadtxt('results/stats_and_rms/m_tot_n_results.dat')
data['time'] = tmp

tmp = np.loadtxt('results_tw/stats_and_rms/m_tot_n_results.dat')
data['time-tw'] = tmp

tmp = np.loadtxt('results_sec_order/stats_and_rms/m_tot_n_results.dat')
data['time-sec'] = tmp

times = np.loadtxt('results_no_time/times.dat')

cc_pars = np.loadtxt('data/cc_pars.dat')
fig, ax = plt.subplots(1, 1)

msizes = [10,5,  5, 3]
cc_m_norm = cc_pars[:, 1] / cc_pars[0, 1]
#cc_m_n = cc_pars[:, 1] / np.exp(cc_pars[:, 0])

ax.scatter(times, cc_m_norm, s=70, color='k', label='original')
#ax.scatter(times, cc_m_n, s=70, color='k')
for nr, key in enumerate(data.keys()):
    data_norm = data[key] / data[key][0]
    ax.plot(times, data_norm, '.-', label=key, markersize=msizes[nr])

ax.set_ylabel('NORMED mtotn')
ax.legend(loc='lower left')

fig.savefig('comparison_mtotn.png', dpi=300)
