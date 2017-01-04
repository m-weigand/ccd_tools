from NDimInv.plot_helper import *
import numpy as np
import scipy
from scipy import stats
import lib_dd

f = np.logspace(-3, 4, 100)
tau = np.logspace(-5,2,100) # create tau distribution
s = np.log10(tau) # natural logarithm
settings = {
     'Nd': 20,
     'tau_values': tau,
     'frequencies': f,
     'tausel': 'data_ext',
     'c': 1.0,
}
model = lib_dd.models.ccd_res.decomposition_resistivity(settings)
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

rre_rim = model.forward(pars)
rre = rre_rim[:, 0]
rim = rre_rim[:, 1]

np.random.rand(5)
# add 5% noise
re_noised = rre + np.random.rand(rre.shape[0]) * 0.05  * rre
im_noised = rim + np.random.rand(rim.shape[0]) * 0.05  * rim

ax.semilogx(f, rre)
ax.semilogx(f, re_noised)
ax.set_xlabel('frequencies (Hz)')
ax.set_ylabel(r'$Re(\rho) (\Omega m)$')
ax = fig.add_subplot(223)
ax.semilogx(f, rim)
ax.semilogx(f, im_noised)
ax.set_ylabel(r'$-Im(\rho) (\Omega m)$')
ax = fig.add_subplot(224)
pha = np.arctan(-rim/rre) * 1000
pha_noised = np.arctan(-im_noised/re_noised) * 1000
ax.semilogx(f, -pha)
ax.semilogx(f, -pha_noised)
ax.set_ylabel(r'$-Phase (mrad)$')

fig.subplots_adjust(hspace=0.3, wspace=0.4)
fig.show()