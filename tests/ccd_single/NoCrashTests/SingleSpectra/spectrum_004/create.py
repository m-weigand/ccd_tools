#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
from NDimInv.plot_helper import *
import numpy as np
import scipy
from scipy import stats
import sys
sys.path.append('../../../')
import dd_resistivity
dd_res = dd_resistivity.dd_resistivity()

tau = np.logspace(-5,2,100) # create tau distribution
s = np.log10(tau)
mean = 0
std = 1.5
m = stats.norm.pdf(s, mean, std) / 100 + \
   stats.norm.pdf(s, -4.5, 1.5) / 50

f = np.logspace(-3, 4, 100)
pars = np.hstack((100, m))
omega = f * 2 * np.pi

re,im = dd_res.calculate_reim(omega, pars, np.log10(tau))
mag = np.abs(re + 1j * -im)
pha = np.arctan(-im/re) * 1000 # mrad

np.savetxt('spectrum.dat', np.hstack((mag,pha))[np.newaxis, :])
np.savetxt('frequencies.dat', f)

# plot
fig = plt.figure()

ax = fig.add_subplot(221)
ax.semilogx(tau, m)
ax.set_xlabel(r'$\tau_i$')
ax = fig.add_subplot(222)

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
fig.savefig('spectrum.png')

