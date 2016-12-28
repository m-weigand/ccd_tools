from NDimInv.plot_helper import *
import numpy as np
import scipy
from scipy import stats
import lib_dd

f = np.logspace(-3, 4, 100)
tau = np.logspace(-5,2,100) # create tau distribution
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
np.random.rand(5)
# add 5% noise
re_noised = re + np.random.rand(re.shape[0]) * 0.05  * re
im_noised = im + np.random.rand(im.shape[0]) * 0.05  * im

ax.semilogx(f, re)
ax.semilogx(f, re_noised)
ax.set_xlabel('Frequencies (Hz)')
ax.set_ylabel(r'$Re(\rho) (\Omega m)$')
ax = fig.add_subplot(223)
ax.semilogx(f, im)
ax.semilogx(f, im_noised)
ax.set_ylabel(r'$-Im(\rho) (\Omega m)$')
ax = fig.add_subplot(224)
pha = np.arctan(-im/re) * 1000
pha_noised = np.arctan(-im_noised/re_noised) * 1000
ax.semilogx(f, -pha)
ax.semilogx(f, -pha_noised)
ax.set_ylabel(r'$-Phase (mrad)$')

fig.subplots_adjust(hspace=0.3, wspace=0.4)
fig.show()