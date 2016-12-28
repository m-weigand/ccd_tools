from NDimInv.plot_helper import *
import numpy as np
import scipy
from scipy import stats
import sys
import lib_dd

f = np.logspace(-3, 4, 100)
tau = np.logspace(-5, 2, 100) # create tau distribution
s = np.log10(tau) # natural logarithm
settings = {'Nd': x,
            'tau_values': tau,
            'frequencies': f,
            'tausel': 'data_ext'
            }
model = lib_dd.main.get('log10rho0log10m', settings)
# tau-distribtution, mean, std
m = stats.norm.pdf(s, 0, 1.5) / 100 + \
    stats.norm.pdf(s, -4.5, 1.5) / 50
g = np.log10(m)

fig = plt.figure()

# m distribution
ax = fig.add_subplot(221)
ax.semilogx(tau, m)
ax.set_xlabel(r'$\tau_i$')
ax.set_ylabel('m')

ax = fig.add_subplot(222)
pars = np.hstack((100, g))
omega = f * 2 * np.pi

re, im = model.forward_re_mim(pars)
ax.semilogx(f, re)
ax.set_xlabel('Frequencies (Hz)')
ax.set_ylabel(r'$Re(\rho) (\Omega m)$')
ax = fig.add_subplot(223)
ax.semilogx(f, im)
ax.set_ylabel(r'$-Im(\rho) (\Omega m)$')
ax = fig.add_subplot(224)
pha = np.arctan(-im/re) * 1000
ax.semilogx(f, -pha)
ax.set_ylabel(r'$-Phase (mrad)$')

fig.subplots_adjust(hspace=0.3, wspace=0.4)
fig.show()