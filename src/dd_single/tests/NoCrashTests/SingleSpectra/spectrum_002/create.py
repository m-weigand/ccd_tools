#!/usr/bin/python

import numpy as np
import crlab_py.colecole as colecole

frequencies = np.logspace(-3,4,40)
fin = np.hstack((frequencies, frequencies))

cc_pars = np.array( (np.log(100),
                     0.08,
                     np.log(0.10),
                     1,
                     ))
print(cc_pars)

erg = colecole.cole_log(fin, cc_pars)
print(erg.shape)

erg[0,:] = np.exp((erg[0,:]))

np.savetxt('spectrum.dat', erg.flatten()[np.newaxis, :])
np.savetxt('frequencies.dat', frequencies)
from crlab_py.mpl import *

fig = plt.figure()
ax = fig.add_subplot(211)
ax.semilogx(frequencies, erg[0,:])
ax.set_ylabel('Magnitude (Ohm m)')
ax.set_xlabel('Frequency (Hz)')
ax = fig.add_subplot(212)
ax.semilogx(frequencies, -erg[1,:])
ax.set_ylabel('- Phase (mrad)')
ax.set_xlabel('Frequency (Hz)')
fig.savefig('spectrum.png')
