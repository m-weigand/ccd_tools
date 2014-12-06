#!/usr/bin/python
import numpy as np
import lib_dd.colecole as colecole
from NDimInv.plot_helper import *

frequencies = np.logspace(-3, 4, 40)
fin = np.hstack((frequencies, frequencies))

cc_pars = np.array((np.log(100),  # rho0
                    0.08,        # m
                    np.log(0.10),  # tau
                    1,           # c
                    0.15,
                    np.log(0.0001),
                    1
                    ))
erg = colecole.cole_log(fin, cc_pars)

erg[0, :] = np.exp((erg[0, :]))

np.savetxt('data.dat', erg.flatten()[np.newaxis, :])
np.savetxt('frequencies.dat', frequencies)
