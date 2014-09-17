#!/usr/bin/python
from crlab_py.mpl import *
import numpy as np

settings = {}
settings[0] = (r'$\rho_0~(\Omega m)$', )
settings[1] = (r'$m_{tot}$', )
settings[2] = (r'$m_{tot}^n$', )
settings[3] = (r'$\tau_{peak}$', )

frequencies = np.loadtxt('frequencies.dat')

data = np.loadtxt('pixel_458.dat')

timesteps = range(1, 22)

fig, axes = plt.subplots(2, 1, figsize=(5, 4))

for timedata in data:
    center = timedata.size / 2
    rmag = timedata[0:center]
    rpha = timedata[center:]
    rrho = rmag * np.exp(1j * rpha / 1000)

    # mag/rre
    ax = axes[0]
    ax.loglog(frequencies, np.real(rrho), '.-')
    ax.set_xlabel('frequency (Hz)')
    ax.set_ylabel(r"$\rho'~(\Omega m)$")

    # pha/rim
    ax = axes[1]
    ax.loglog(frequencies, -np.imag(rrho), '.-')
    ax.set_xlabel('frequency (Hz)')
    ax.set_ylabel(r"$\rho''~(\Omega m)$")

for ax in axes:
    ax.set_xlim([np.min(frequencies), np.max(frequencies)])

fig.tight_layout()
fig.subplots_adjust(top=0.9)
fig.savefig('bnk1_spectra.png', dpi=300)
