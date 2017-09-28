import NDimInv.plot_helper
plt, mpl = NDimInv.plot_helper.setup()
import numpy as np
import sys
import lib_dd
import lib_dd.models.ccd_res

f = np.logspace(-3, 6, 100)
tau = np.array((1.5915e-06,))

settings = {'Nd': 20,
            'tau_values': tau,
            'frequencies': f,
            'tausel': 'data_ext',
            'c': 1.0,
            }
model = lib_dd.models.ccd_res.decomposition_resistivity(settings)
m = np.array((np.log10(0.01),))
s = np.log10(tau) # natural logarithm

f_max = 1 / (2 * np.pi * tau[0])

pars = np.hstack((100, m))
omega = f * 2 * np.pi

rre_rim = model.forward(pars)
rre = rre_rim[:, 0].squeeze()
rim = rre_rim[:, 1].squeeze()

fig = plt.figure()
fig.suptitle(r'Minimum frequency $\tau$ selection')
ax = fig.add_subplot(411)
ax.set_xscale('log')
ax.axvline(1e-5)
ax.set_xlabel(r'$\tau_i$')
ax.set_ylabel('m')
ax.set_xlim([1e-6, 1e8])

ax = fig.add_subplot(412)
ax.semilogx(f, rre)
ax.set_ylabel(r'$Re(\rho) (\Omega m)$')
ax.set_xlabel('Frequency (Hz)')

ax = fig.add_subplot(413)
ax.semilogx(f, rim)
ax.axvline(f_max, color='r')
ax.set_ylabel(r'$-Im(\rho) (\Omega m)$')
ax.set_xlabel('Frequency (Hz)')

ax = fig.add_subplot(414)
pha = np.arctan(-rim/rre) * 1000
ax.semilogx(f, -pha)
ax.set_ylabel(r'$-Phase (mrad)$')
ax.set_xlabel('Frequency (Hz)')

fig.subplots_adjust(hspace=0.7, wspace=0.4)
fig.show()