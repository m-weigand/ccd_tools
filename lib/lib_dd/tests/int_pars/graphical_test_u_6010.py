#!/usr/bin/python
import pylab as plt
# import matplotlib as mpl
import numpy as np

import lib_dd.int_pars as IP

print dir(IP)

N = 10
tau = np.logspace(-4, 4, N)
s = np.log10(tau)

rho0 = 100.0
# m = np.ones_like(tau)
m = np.array((1, 1, 1, 1, 1,
              1, 1, 1, 1, 1))

# m[0: int(N / 2)] = 1
# m[int(N / 2): 2] = 2

pars = np.hstack((rho0, m))
print pars
print IP._m_tot_n_linear(pars, tau, s)
cums_gtau = IP._cumulative_tau(pars, tau, s)
norm = np.abs(cums_gtau).max()
a = cums_gtau / norm

# plot tau,
fig, ax = plt.subplots(1, 1, figsize=(7, 4))

ax.semilogx(tau, m, '.-', label='RTD', color='k')

ax.semilogx(tau, cums_gtau, '.-', label='cums_gtau')

colors = ('r', 'g', 'b', 'y', 'c')

for nr, x in enumerate((0.2, 0.4, 0.6, 0.8)):
    s_x, f_x, index = IP._tau_x(x, pars, tau, s)
    print 'result', index
    ax.axvline(x=10 ** s_x, label=x, color=colors[nr % colors.__len__()])
    ax.axhline(y=x, color='k')

ax.legend(loc="lower center",
          ncol=4,
          bbox_to_anchor=(0, 0, 1, 1),
          bbox_transform=fig.transFigure)

fig.tight_layout()
fig.subplots_adjust(bottom=0.3)
fig.savefig('check_u_taux.png', dpi=300)
