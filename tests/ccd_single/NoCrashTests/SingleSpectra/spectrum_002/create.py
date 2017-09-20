#!/usr/bin/env python
import numpy as np
import NDimInv.plot_helper
plt, mpl = NDimInv.plot_helper.setup()
import lib_cc2.cc as cc

frequencies = np.logspace(-3, 4, 40)
colecole = cc.colecole(frequencies)

colecole.set_parameters((np.log(100),
                         0.08,
                         np.log(0.10),
                         1,
                         ))
erg = np.array(colecole.mag_pha())

np.savetxt('data.dat', erg.flatten()[np.newaxis, :])
np.savetxt('frequencies.dat', frequencies)
