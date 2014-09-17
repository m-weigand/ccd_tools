Best practices
--------------

The following procedure is recommended for new data sets and focuses on
inversions using *dd_single.py* and *dd_time.py*:

* Invert with variable :math:`\lambda` values for the frequency regularization
* Fine-tune with a fixed lambda (this in general yields more robust results and
  makes results comparable)
* for time regularization: here only a fixed lambda can be used. Start with a
  small value and take a look at the maximum regularization strength for the
  time-regularization. The regularization strength is automatically plotted
  when the ``--plot`` option is enabled.


Formulation in resistivities
----------------------------

.. toctree::

    dd_formulations_res

Statistical parameters
----------------------

* :math:`m_{tot} = \sum_i^N m_i`
* :math:`m_{tot}^n = \frac{m_{tot}}{\rho_0}`
* :math:`tau_{50}`
* :math:`\tau_{mean} = \frac{exp(\sum_i m_{sel}^i \cdot log(\tau_{sel}^i))}{\sum m_{sel}^i}`

Creating synthetic :math:`g_i` distributions
--------------------------------------------

The :math:`\tau_i` distribution is determined by the frequencies of the data
and number of values per frequency decade set by the user. For synthetic
studies or benchmarks we need to set the corresponding :math:`g_i` values for
those relaxation times. We do this either by explicitly setting those
relaxation times for a small number of terms (usually one to three in
correspondence to the Cole-Cole/Debye model), or by addition of one or more
log-normal distributions to the :math:`g_i` distribution.

.. plot::

   from NDimInv.plot_helper import *
   import numpy as np
   import scipy
   from scipy import stats
   import sys
   import lib_dd.main as dd_res

   f = np.logspace(-3, 4, 100)
   tau = np.logspace(-5, 2, 100) # create tau distribution
   s = np.log10(tau) # natural logarithm
   settings = {'tau_values': tau,
               'frequencies': f
               }
   dd_res = dd_res.get('log10rho0log10m', settings)
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

   re, im = dd_res.forward_re_mim(pars)
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
   fig.show()


Normally distributed noise can then be added to this spectrum:

.. plot::

   from NDimInv.plot_helper import *
   import numpy as np
   import scipy
   from scipy import stats
   import lib_dd.main as dd_res

   f = np.logspace(-3, 4, 100)
   tau = np.logspace(-5,2,100) # create tau distribution
   s = np.log10(tau) # natural logarithm
   settings = {'tau_values': tau,
               'frequencies': f
               }
   dd_res = dd_res.get('log10rho0log10m', settings)
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

   dd_res.frequencies = f
   dd_res.omega = omega
   dd_res.tau = tau
   dd_res.s = np.log10(tau)
   re, im = dd_res.forward_re_mim(pars)
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

:math:`f_{max}` for imaginary part
----------------------------------

Notes:

.. math::

    f(x) &= \frac{u(x)}{v(x)}\\
    f'(x) &= \frac{u'(x) v(x) - u(x) v'(x)}{v^2(x)}

Determine the frequency maximum of the negative of the imaginary part using the
first derivation:

.. math::

    Im(\hat{\rho}(\omega)) &= -  \rho_0 \sum_{i=1}^N m_i \frac{(\omega \tau_k)}{1 + (\omega \tau_k)^2}\\
    \frac{\partial Im}{\partial \omega} &= \frac{\partial_\omega (-\rho_0 m \omega \tau) [1 + (\omega \tau)^2] - (-\rho_0 m \omega \tau) \partial_\omega (1 + (\omega \tau)^2)}{[1 + (\omega \tau)^2]^2}\\
    &= \frac{(-\rho_0 m \tau) [1 + (\omega \tau)^2] + \rho_0 m \omega \tau \cdot 2 \omega \tau \tau}{[1 + (\omega \tau)^2]^2}\\
    \Rightarrow \frac{\partial -Im}{\partial \omega} &= 0\\
    &\Leftrightarrow - \rho_0 m \tau - \rho_0 m \tau (\omega \tau)^2 + 2 \omega^2 \tau^3 m \rho_0 = 0\\
    & / \tau / \rho_0 / m\\
    &\Rightarrow -1 - \omega^2 \tau2 + 2 \omega^2 \tau^2 = 0\\
    &\Rightarrow \omega^2 \cdot (2 - 1) \tau^2 = 1\\
    &\Rightarrow \omega^2 = \frac{1}{(2-1) \tau^2}\\
    &\Rightarrow \omega = \pm \frac{1}{\tau}
    \text{Negative } \omega \text{ not possible}\\
    &\Rightarrow \omega_{max} = \frac{1}{\tau_{max}}\\
    &\Leftrightarrow f_{max} = \frac{1}{2 \pi \tau_{max}}\\
    &\Leftrightarrow \tau_{max} = \frac{1}{2 \pi f_{max}}


:math:`\tau` ranges to consider
-------------------------------

The following approach to select :math:`\tau` values is called 'data'

For forward modelling and inversions there is always the question of which
range of relaxation times to consider. To answer this we consider the typical
frequency range of measurements from 1 mHz to 50 kHz. By considering one-term
debye models we can compute the minimum and maximum :math:`\tau` values using
the formula:

.. math::

    \tau_{peak} = \frac{1}{2 \pi f_{peak}}\\
    \tau_{min}(0.001~Hz) &= 159.15~s\\
    \tau_{max}(1e5~Hz) &= 1.5915e-06~s


For the implementation the number of :math:`\tau` values :math:`N_D` per decade
is specified. The maximum :math:`\tau`-interval corresponds to the frequency
range :math:`[1e-3~s, 1e5~s]`. Now compute the total number :math:`N` of
:math:`\tau` values using the formula

.. math::

    N = |log_{10}(f_{min}) - log_{10}(f_{max})| \cdot N_D

.. note::

    The maximum frequency range considered here spans exactly 8 decades. Thus
    no rounding needs to take place.

The pool of possible :math:`\tau` values is now created by

::

    np.logspace(-3,5,N_D)

The :math:`\tau` values for a real data set will now be selected from this
pool, depending on the minimum and maximum frequency of the data set. This
procedure ensures that always the same :math:`\tau` values are used
independently from the minimum and maximum data frequencies. However, the
:math:`\tau` values will still be dependend on :math:`N_D`!

.. plot::

    from NDimInv.plot_helper import *
    import numpy as np
    import sys
    import lib_dd.main as dd_res

    f = np.logspace(-3, 6, 100)
    tau = np.array((1.5915e-06,))
    settings = {'tau_values': tau,
               'frequencies': f
               }
    dd_res = dd_res.get('log10rho0log10m', settings)
    m = np.array((np.log10(0.01),))
    s = np.log10(tau) # natural logarithm

    f_max = 1 / (2 * np.pi * tau[0])

    pars = np.hstack((100, m))
    omega = f * 2 * np.pi

    dd_res.frequencies = f
    dd_res.omega = omega
    dd_res.tau = tau
    dd_res.s = np.log10(tau)
    re, im = dd_res.forward_re_mim(pars)

    fig = plt.figure()
    fig.suptitle(r'Minimum frequency $\tau$ selection')
    ax = fig.add_subplot(411)
    ax.set_xscale('log')
    ax.axvline(1e-5)
    ax.set_xlabel(r'$\tau_i$')
    ax.set_ylabel('m')
    ax.set_xlim([1e-6, 1e8])

    ax = fig.add_subplot(412)
    ax.semilogx(f, re)
    ax.set_ylabel(r'$Re(\rho) (\Omega m)$')
    ax.set_xlabel('Frequency (Hz)')

    ax = fig.add_subplot(413)
    ax.semilogx(f, im)
    ax.axvline(f_max, color='r')
    ax.set_ylabel(r'$-Im(\rho) (\Omega m)$')
    ax.set_xlabel('Frequency (Hz)')

    ax = fig.add_subplot(414)
    pha = np.arctan(-im/re) * 1000
    ax.semilogx(f, -pha)
    ax.set_ylabel(r'$-Phase (mrad)$')
    ax.set_xlabel('Frequency (Hz)')

    fig.subplots_adjust(hspace=0.7, wspace=0.4)
    fig.show()

.. plot::

   from NDimInv.plot_helper import *
   import numpy as np
   import lib_dd.main as dd_res

   tau = np.array((159.15,))
   f_max = 1 / (2 * np.pi * tau[0])
   s = np.log10(tau)

   m = np.array((np.log10(0.01),))
   f = np.logspace(-5, 6, 100)
   settings = {'tau_values': tau,
              'frequencies': f
              }
   dd_res = dd_res.get('log10rho0log10m', settings)
   pars = np.hstack((100, m))
   omega = f * 2 * np.pi

   dd_res.frequencies = f
   dd_res.omega = omega
   dd_res.tau = tau
   dd_res.s = np.log10(tau)

   re, im = dd_res.forward_re_mim(pars)

   fig = plt.figure()
   fig.suptitle('Minimum frequency $\tau$ selection')

   ax = fig.add_subplot(411)
   ax.set_xlim([1e-6, 1e8])
   ax.set_xscale('log')
   ax.axvline(tau)
   ax.set_xlabel(r'$\tau_i$')
   ax.set_ylabel('m')

   ax = fig.add_subplot(412)
   ax.semilogx(f, re)
   ax.set_ylabel(r'$Re(\rho) (\Omega m)$')
   ax.set_xlabel('Frequency (Hz)')

   ax = fig.add_subplot(413)
   ax.semilogx(f, im)
   ax.set_ylabel(r'$-Im(\rho) (\Omega m)$')
   ax.set_xlabel('Frequency (Hz)')
   ax.axvline(f_max, color='r')

   ax = fig.add_subplot(414)
   pha = np.arctan(-im/re) * 1000
   ax.semilogx(f, -pha)
   ax.set_xlabel('Frequency (Hz)')
   ax.set_ylabel(r'$-Phase (mrad)$')

   fig.subplots_adjust(hspace=0.7, wspace=0.4)
   fig.show()


The following approach to selecting :math:`\tau` values is called 'data_ext'.

This approach adds one frequency decade to each of the frequency limits of the
data prior to converting those limits to :math:`\tau` values.

Literature
----------

DD Implementations:

* Morgan and Lesmes 1994 - Inversion for dielectric relaxation spectra
* S. Nordsiek Bearbeitung und Interpretation von Spektren der Induzierten Polarisation - Dissertation TU Clausthal
* Zisser et al 2010 - Relationship between low-frequency electrical properties and hydraulic permeability of low-permeability sandstones
* Zisser 2010, PhD, Relationship between Hydraulic Permeability and Spectral Electrical Response of Sandstones, University of Bonn
* SERfit manual (Zisser 2009)
* Nordsiek and Weller 2008 - A new approach to fitting induced-polarization spectra
* Attwa M. and Günther T., Spectral induced polarization measurements for predicting the hydraulic conductivity in sandy aquifers, Hydrol. Earth Syst. Sci., 17., 4079 - 4094, 2013
* Flores Orozco et al 2012 - Delineation of subsurface hydrocarbon contamination at a former hydrogenation plant using spectral induced polarization imaging

Misc:

* Tarasov and Titov 2007 - Relaxation time distribution from time domain induced polarization measurements
* Tarasov and Titov 2013 - On the use of the Cole-Cole equations in spectral indcued polarization
* Böttcher and Bordewijk 1978 - Theory of electric parameteritation
* Pelton et al 1978 - Mineral discrimination and removal of inductive coupling with multifrequency IP
* Lesmes and Morgan 2001 - Dielectric spectroscopy sedimentary rocks
* Zisser et al 2010b
* Weller et al 2010a - Estimating permeability of sandstone samples by nuclear magnetic resonance and spectral-induced polarization
* Weller et al 2010b - On the estimation of specific surface per unit pore volume from induced polarization: A robust empirical relation fits multiple data sets
* Revil et al 2012 - Is it the grain size or the characteristic pore size that controls the induced polarization relaxation time of clean sands and sandstones?
* Olhoeft 1985 - Low-frequency electrical properties
* Revil and Florsch 2010 - Determination of permeability from spectral induced polarization in granular media
* Florsch et al 2012 - Direct estimation of the distribution of relaxation times from induced-polarization spectra using a Fourier transform analysis
* de Lima and Sharma 1992

Interesting weighting for CC-fit:

* Kruschwitz et al. 2010 - Textural controls on low-frequency electrical spectra of porous media

Application of DD:

* Andreas Weller, Katrin Breede, Lee Slater, and Sven Nordsiek 2011 - Effect of changing water salinity on complex conductivity spectra of sandstones, Geophysics
* Flores Orozco et al 2012 - Delineation of subsurface hydrocarbon contamination at a former hydrogenation plant using spectral induced polarization imaging
* Attwa M. and Günther T., Spectral induced polarization measurements for predicting the hydraulic conductivity in sandy aquifers, Hydrol. Earth Syst. Sci., 17., 4079 - 4094, 2013

Inversion:

* Dennis and Schnabel - Numerical Methods for Unconstrained Optimization and Nonlinear Equations 1996
* Oldenburg and Li 1994 a - Inversion of induced polarization data
* Oldenburg and Li 1994 b - Subspace linear inverse method

Drafts of interesting papers:

* Öberdörster et al 201X - Structural and Lithological Soil Characterization using Spectral Induced Polarization Imaging with Subsequent Debye Decomposition at the Field Scale
* Tarasov and Titov - On the use of the Cole-Cole equations in spectral induced polarization
