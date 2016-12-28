import os
os.environ['DD_USE_LATEX'] = "1"
from NDimInv.plot_helper import *
import numpy as np

frequencies  = np.loadtxt('example2_time/data/frequencies.dat')
data  = np.loadtxt('example2_time/data/data.dat')

fig, axes = plt.subplots(2, 1)
for spectrum in data:
    subdata = spectrum.reshape((2, spectrum.size / 2)).T
    ax = axes[0]
    ax.semilogx(frequencies, subdata[:, 0], '.-', color='k')
    ax = axes[1]
    ax.semilogx(frequencies, -subdata[:, 1], '.-', color='k')

for ax in axes:
    ax.set_xlabel('frequency [Hz]')
axes[0].set_ylabel(r"$|\rho| [\Omega m]$")
axes[1].set_ylabel(r"$\phi [mrad]$")
fig.tight_layout()