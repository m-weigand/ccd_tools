Usage and implementation details
================================

.. toctree::

    data_formats
    starting_models

Best practices
--------------

The following procedure is recommended for new data sets and focuses on
inversions using *ccd_single* and *ccd_time*:

* Initially invert with variable :math:`\lambda` values for the frequency
  regularization
* Fine-tune with a fixed lambda (this in general yields more robust results and
  makes results comparable)
* Usually the third starting model yields the most robust results: ::

    DD_STARTING_MODEL=3 dd_single.py ...

* Normalization can help... : ::

    ccd_single --norm 10

* For time regularization: here only a fixed lambda can be used. Start with a
  small value and take a look at the maximum regularization strength for the
  time-regularization. The regularization strength is automatically plotted
  when the ``--plot`` option is enabled.

* while the structure of the input files is fixed, the data format can be
  changed using the ``--data_format`` option. Thus a conversion from
  conductivities to resistivities and vice versa is not necessary, as well as a
  conversion between real/imaginary part and magnitude/phase format.

* the ``--tmp`` option can improve execution speed on conventional hard
  drives (for SSDs there shouldn't be any improvement)


Normalization
-------------

The CDD is linear in :math:`\rho_0/\sigma_\infty`, as as such data can be
normalized both in magnitude/phase, or real and imaginary parts:

.. math::

    \rho'_{norm} &= A \cdot \rho'\\
    \rho''_{norm} &= A \cdot \rho''\\
    \rho'(\omega)_{norm} &= A \cdot \left(\rho_0 -  \rho_0 \sum_{i=1}^N m_i
 \frac{(\omega \tau_i)^2}{1 + (\omega \tau_i)^2}\right)\\
    \rho''(\omega)_{norm} &= A \cdot \left(- \rho_0 \sum_{i=1}^N m_i \frac{(\omega
 \tau_k)}{1 + (\omega \tau_k)^2} \right)

The factor A is determined by norming the lowest frequency
:math:`\rho'|\sigma'` value to the target value B given by the `--norm` switch:

.. math ::

    A = \frac{B}{\rho'/\sigma'}

Determining relaxation time ranges
----------------------------------

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

.. plot::

   import NDimInv.plot_helper
   plt, mpl = NDimInv.plot_helper.setup()
   import numpy as np
   import lib_dd

   tau = np.array((159.15,))
   f_max = 1 / (2 * np.pi * tau[0])
   s = np.log10(tau)

   m = np.array((np.log10(0.01),))
   f = np.logspace(-5, 6, 100)

   settings = {'Nd': 20,
               'tau_values': tau,
               'frequencies': f,
               'tausel': 'data_ext',
               'c': 1.0,
               }
   model = lib_dd.models.ccd_res.decomposition_resistivity(settings)
   pars = np.hstack((100, m))
   omega = f * 2 * np.pi

   rre_rim = model.forward(pars)
   rre = rre_rim[:, 0]
   rim = rre_rim[:, 1]

   fig = plt.figure()
   fig.suptitle('Minimum frequency $\tau$ selection')

   ax = fig.add_subplot(411)
   ax.set_xlim([1e-6, 1e8])
   ax.set_xscale('log')
   ax.axvline(tau)
   ax.set_xlabel(r'$\tau_i$')
   ax.set_ylabel('m')

   ax = fig.add_subplot(412)
   ax.semilogx(f, rre)
   ax.set_ylabel(r'$Re(\rho) (\Omega m)$')
   ax.set_xlabel('Frequency (Hz)')

   ax = fig.add_subplot(413)
   ax.semilogx(f, rim)
   ax.set_ylabel(r'$-Im(\rho) (\Omega m)$')
   ax.set_xlabel('Frequency (Hz)')
   ax.axvline(f_max, color='r')

   ax = fig.add_subplot(414)
   pha = np.arctan(-rim/rre) * 1000
   ax.semilogx(f, -pha)
   ax.set_xlabel('Frequency (Hz)')
   ax.set_ylabel(r'$-Phase (mrad)$')

   fig.subplots_adjust(hspace=0.7, wspace=0.4)
   fig.show()


The following approach to selecting :math:`\tau` values is called 'data_ext'.

This approach adds one frequency decade to each of the frequency limits of the
data prior to converting those limits to :math:`\tau` values.

Using the Cole-Cole distribution
--------------------------------

A single-termin Cole-Cole spectrum with c = 0.5 was fitted using kernel
functions of c = (0.3, 0.5, 0.7, and 1.0).

* c = 0.3:

  The kernel function is too wide to fit the response:

  .. image:: Fit_responses/results_ddc_0.3/plot_spec_000_iteration0001.png

* c = 0.5

  The kernel function has the same slope as the response. Any widening of the
  peak in the RTD is due to regularisation smoothing.

  .. image:: Fit_responses/results_ddc_0.5/plot_spec_000_iteration0012.png

* c = 0.7

  .. image:: Fit_responses/results_ddc_0.7/plot_spec_000_iteration0004.png

* c = 1.0

  .. image:: Fit_responses/results_ddc_1.0/plot_spec_000_iteration0004.png

Creating synthetic relaxation time distributions
------------------------------------------------

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
   import lib_dd

   f = np.logspace(-3, 4, 100)
   tau = np.logspace(-5, 2, 100) # create tau distribution
   s = np.log10(tau) # natural logarithm
   settings = {'Nd': 20,
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

   ax.semilogx(f, rre)
   ax.set_xlabel('frequencies (Hz)')
   ax.set_ylabel(r'$Re(\rho) (\Omega m)$')
   ax = fig.add_subplot(223)
   ax.semilogx(f, rim)
   ax.set_ylabel(r'$-Im(\rho) (\Omega m)$')
   ax = fig.add_subplot(224)
   pha = np.arctan(-rim/rre) * 1000
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


