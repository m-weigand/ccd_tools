import os
os.environ['DD_USE_LATEX'] = "1"
from NDimInv.plot_helper import *
import numpy as np

frequencies  = np.loadtxt('example1_single/frequencies.dat')
data  = np.loadtxt('example1_single/data.dat')
data = data.reshape((2, data.size / 2)).T

fig, axes = plt.subplots(2, 1)
ax = axes[0]
ax.semilogx(frequencies, data[:, 0], '.', color='k')
ax.set_xlabel('frequency [Hz]')
ax.set_ylabel(r"$|\rho| [\Omega m]$")
ax = axes[1]
ax.semilogx(frequencies, -data[:, 1], '.', color='k')
ax.set_xlabel('frequency [Hz]')
ax.set_ylabel(r"$\phi [mrad]$")
fig.tight_layout()