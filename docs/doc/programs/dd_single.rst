dd_single.py
============

.. toctree::
    :hidden:

    dd_testing_res_inv

This program is used to fit one or multiple
SIP-spectra in one go. There is no regularization between the spectra.

For detailed information on command line options and usage please refer to the
sections below. Also note the :ref:`ref_dd_single_best_pract` section.

Command line options
--------------------

.. program-output:: dd_single.py -h

Usage Examples
--------------

.. note::

    Beware of the chargeability distribution at the frequency edges: Here the
    distribution is often dominated by the starting model due to low
    sensitivities. However it is advisable to add one frequency decade in
    :math:`\tau` values to the edges.

.. _ref_dd_single_best_pract:

Best practices
~~~~~~~~~~~~~~

* while the structure of the input files is fixed, the data format can be
  changed using the ``--data_format`` option. Thus a conversion from
  conductivities to resistivities and vice versa is not necessary, as well as a
  conversion between real/imaginary part and magnitude/phase format.

* the ``--tmp`` option can improve execution speed on conventional hard
  drives (for SSDs there shouldn't be any improvement)


Usage exmaple 1
~~~~~~~~~~~~~~~

You need a frequency file which contains the frequencies, each in a seperate
line, in ascending order:

frequency.dat: ::

    0.463
    1.000
    2.128
    4.545
    10.000
    14.706
    21.277
    27.778
    29.412
    50.000
    58.824
    70.000

Complex resistivity spectra are provided using a data file which holds a
spectrum in each line. Columns are separated by space and values are linear
both for magnitude and phase values. The first N columns correspond to the
magnitude values (:math:`\Omega m`) corresponding to the frequencies stored in
*frequencies.dat*. The following N columns represent the corresponding phase
values.

data.dat: ::

    17.9984 17.9897 17.9792 17.9636 18.0217 18.0235 18.0817 18.0135 18.0854 18.0856 18.0816 18.0802 18.0777 18.0770 18.0747 18.0748 18.0748 18.0738 18.0757 18.0790 -1.2674 -2.1537 -2.7997 -3.7206 -3.1617 -3.8350 -0.2499 -3.8007 -3.7300 -2.9362 -3.4580 -3.3821 -3.1575 -3.0282 -3.0008 -2.7883 -2.7889 -2.6931 -2.3717 -1.9792
    17.9983 17.9896 17.9790 17.9633 18.0217 18.0235 18.0817 18.0135 18.0854 18.0856 18.0816 18.0802 18.0777 18.0769 18.0747 18.0748 18.0747 18.0738 18.0757 18.0790 -1.2790 -2.1838 -2.8497 -3.7900 -3.2634 -3.9336 -0.2695 -3.8899 -3.8167 -2.9599 -3.5263 -3.4432 -3.2061 -3.0744 -3.0456 -2.8269 -2.8222 -2.7246 -2.3927 -1.9903

The spectra can now be fitted to a Debye decomposition using the command:

::

    dd_single.py -f frequencies.dat -d data.dat -o dd_results/

Results will be written to the subdirectory **dd_results/**

.. _ref_dd_single_output_format:

Output Files
============

The following output files will be created in the selected output directory.
These files are described below, sorted by category.

Input data
----------

* *data.dat* contains the input data, converted to :math:`\sigma';\sigma''~(S/m)`.
* *data_format.dat* contains the data format in the format usable with the
  ``--data_format`` command line option.
* Frequencies and corresponding angular frequencies (
   :math:`\omega = 2 \cdot \pi \cdot f`) are stored in the files
   *frequencies.dat* and *omega.dat*.
* The file *command.dat* holds the complexe call to the fit routine
* A JSON formatted file *inversion_options.json* stores internal inversion
  options. This file is mainly for debugging purposes, and needed to recreated
  inversion objects from fit results.

Filter results
--------------

* *filter_mask.dat* contains the remaining indices after a filter operation
  with `ddps.py`

Primary fit results
-------------------

* :math:`\tau` and :math:`s = log_{10}(\tau)` values are stored in the files
  *tau.dat* and *s.dat*, respectively.

* The regularization parameters of the last iterations are stored in the file
  *lambdas.dat*, one per line:

  ::

    1.000000000000000021e-03
    1.000000000000000056e-01

* The chargeability values of the last iteration can be found in
  *stats_and_rms/m_i_results.dat*

* The forward response of the final iteration is stored in *f.dat*

* RMS values are stored in the subdirectory *stats_and_rms*, using the
  following files (final RMS of each spectrum per line). *part1/part2* here
  correspond to real part and imaginary part of resistivity, respectively. The
  *_err* suffix denotes RMS values computed with data weighting.

  ======================  ==========================================================
  filename                description
  ======================  ==========================================================
  *rms_both_err.dat*      RMS of real and imaginary parts, including error weighting
  *rms_both_no_err.dat*
  *rms_part1_err.dat*
  *rms_part1_no_err.dat*
  *rms_part2_err.dat*
  *rms_part2_no_err.dat*
  ======================  ==========================================================

    .. math::

        RMS_{\text{no error}} = \sqrt{\frac{1}{N} \sum_i^N d_i - f_i(m)}\\
        RMS_{\text{with error}} = \sqrt{\frac{1}{N} \sum_i^N \frac{d_i - f_i(m)}{\epsilon_i}}

* The number of iterations for each spectrum are stored in *nr_iterations.dat*

* Data weighting errors are stored in *errors.dat*



Integrated parameters
---------------------

Statistical parameters are stored in the subdirectory *stats_and_rms*, and all
output files have the same file format. Each line contains the value of one
spectrum. This applies to the following files:

=============================  ===============================
filename                       stored values per line
=============================  ===============================
*m_i_results.dat*              :math:`m(\tau_i)`
*m_tot_n_results.dat*          :math:`log_{10}(m_{tot}^n)`
*m_tot_results.dat*            :math:`log_{10}(m_{tot}^n)`
*rho0_results.dat*             :math:`log_{10}(\rho_0)`
*tau_50_results.dat*           :math:`log_{10}(\tau_50)`
*tau_mean_results.dat*         :math:`log_{10}(\tau_{mean})`
*tau_arithmetic_results.dat*   :math:`log_{10}(\tau_{arithmetic})`
*tau_geometric_results.dat*    :math:`log_{10}(\tau_{geometric})`
*tau_peak1_results.dat*        :math:`log_{10}(\tau_{peak}^1)`
*tau_peak2_results.dat*        :math:`log_{10}(\tau_{peak}^2)`
*tau_peaks_all_results.dat*    :math:`log_{10}(\tau_{peak}^i)`
*tau_x_\*.dat*                 :math:`log_{10}(\tau_x)`; see description below
*tau_max.dat*                  :math:`\tau` corresponding to max. chargeability. First occurence.
*U_tau_results.dat*            Uniformity parameter :math:`U_{\tau}`
*f_50_results.dat*
*f_mean_results.dat*
*f_peak1_results.dat*
*f_peak2_results.dat*
*f_peaks_all_results.dat*
*covf_results.dat*
*covm_results.dat*
=============================  ===============================

**:math:`\tau_x`** Arbitrary cumulative relaxation times can be computed by setting
the environment variable **DD_TAU_X**. The string separates the requested
percentages as fractions with ';' characters.

Example:

::

    DD_TAU_X="0.2;0.35;0.6" dd_single.py

*Integrated parameters* extracted from the RTD fall into two categories:
chargeability related values and relaxation time related values.  The first
category extracts information regarding the total or partial polarization
strength of the system, while the second extracts information regarding
relaxation times, i.e. the time scales on which the polarization processes take
place:

**Chargeability parameters:**

* The total chargeability :math:`m_{tot} = \sum_i^N m_i` is the analogon of the
  DD to the chargeability as defined by Seigel, 1959:
  :math:`m_{seigel} = \frac{\epsilon_{\infty} - \epsilon_0}{\epsilon_{\infty}}
  = \frac{\rho_0 - \rho_{\infty}}{\rho_0}` (this is also the definition used
  for :math:`m_{cc}`).  This is, howoever, only true insofar as the majority of
  the polarisation response of the system must be located within the measured
  frequency range for the DD to pick it up, while the original definition of
  the chargeability extends over the whole frequency domain. Thus, not fully
  resolved polarization peaks indicate an underestimation of the total
  polarization of the system by :math:`m_{tot}` in the DD.
* Nordsiek and Weller, 2008 computed chargeability sums for each
  relaxation time decades, normed by :math:`m_{tot}`. These so called *decade
  loadings* provide frequency (or relaxation time) dependent chargeabilities.
* The total, normalized chargeability :math:`m_{tot}^n =
  \frac{m_{tot}}{\rho_0}` is obtained by normalizing the total chargeability
  with the DC resistivity (:raw-tex:`\citet{scott2003phd},
  \citet{weller2010g_a}`). It gives an indication of the total polarization of
  the measured system without any influence of any occuring resistivity contrasts.

**Relaxation time parameters:**

Various parameters to determine characteristic relaxation times from the whole
RTD were proposed:

* Cumulative relaxation times :math:`\tau_x` denote relaxation times at which a
  certain percentage :math:`x` of chargeability is reached
  (Norsieg and Weller, 2008; Zisser et al. 2010). For example,
  :math:`\tau_{50}` is the median relaxation time of a given RTD.
* Nordsiek and Weller, 2008 introduced the non-uniformity parameter
  :math:`U_\tau = \frac{\tau_{10}}{\tau_{60}}` which characterizes the width of
  the RTD. However, no information regarding the number of siginificant peaks
  in the RTD can be derived using :math:`U_{\tau}`.
* Tong et al, 2004 use the arithmetic and geometric means of the relaxation
  times for further analysis:

  .. math::

      \tau_g = \left(\prod_{i=1}^N \tau_i^{m_i} \right)^{\frac{1}{\sum_{i=1}^N
      m_i}}\\
      \tau_a = \frac{\sum_{i=1}^N m_i \cdot \tau_i}{\sum_{i=1}^N m_i}

* :raw-tex:`\citet{nordsiek2008seg}` introduced the logarithmic average
  relaxation time :math:`\tau_{mean}`

  .. math::

      \tau_{mean} = \frac{exp(\sum_i m_i \cdot log(\tau_i))}{\sum m_i}`

The listed relaxation time parameters do not take into account the specific
shape of the RTD, and thus it is also useful to determine local maxima of the
distribution, e.g. to extract characteristic relaxation times specific to
certain polarisation peaks. This approach has conceptual similarities to the
use of (multi-)Cole-Cole models as the produced relaxation times can be
directly related to polarization peaks. The relaxation time with the larges
corresponding chargeability is called :math:`\tau_{max}`
:raw-tex:`\citet{attwa2013hess}`, and the in the generalized form the
relaxation time :math:`\tau_{peak}^i`, refers to the *i*-th local maximum of
the RTD, starting with the low frequencies (i.e. high :math:`\tau` values).
This approach can recover multiple peaks without any knowlegdge of the exact
number of peaks in the data.  However, this process can yield multiple small
maxima if the smoothing between adjacent chargeabilitiy values is not strong
enough. In these cases the corresponding smoothing parameters of the DD should
be increased.

Starting model
==============

The following methods can be used to determine starting models. A specific
method can be selected by setting the environment variable
**DD_STARTING_MODEL** to the corresponding integer number, i.e.:

::

    DD_STARTING_MODEL=3 dd_single.py ...

* (`DD_STARTING_MODEL = 1`): Flat starting model
* (`DD_STARTING_MODEL = 2`): [TODO] (Gaussian, center at peak of imaginary part)
* (`DD_STARTING_MODEL = 3`): [TODO] (Frequency decade wise approximation)


Testing
=======

See :doc:`dd_testing_res_inv`

Formulation in resistivities
============================

:doc:`../dd_formulations_res`

Jacobian
========

The Jacobian of :math:`\underline{f}(\underline{m})` is defined as:

.. math::

  \underline{\underline{J}}_{ij} = \begin{pmatrix}\underline{\frac{\partial Re(\hat{\rho}(\omega_i))}{\partial p_j}}\\\underline{\frac{\partial -Im(\hat{\rho}(\omega_i))}{\partial p_j}}\end{pmatrix}

As such it is a (2 F x M) matrix, with F the number of frequencies and M the number of patameters.

.. math::

  \underline{\underline{J}}^{Re}_{linear} &= \begin{bmatrix} \frac{\partial Re(\hat{\rho}(\omega_1))}{\partial \rho_0} & \frac{\partial Re(\hat{\rho}(\omega_1))}{\partial g_1} & \cdots & \frac{\partial Re(\hat{\rho}(\omega_1))}{\partial g_P}\\ \vdots & \ddots & & \vdots\\ \frac{\partial Re(\hat{\rho}(\omega_m))}{\partial \rho_0} & \frac{\partial Re(\hat{\rho}(\omega_m))}{\partial g_1} & \cdots & \frac{\partial Re(\hat{\rho}(\omega_m))}{\partial g_P} \end{bmatrix}\\
  \underline{\underline{J}}^{-Im}_{linear} &= \begin{bmatrix} \frac{\partial -Im(\hat{\rho}(\omega_1))}{\partial \rho_0} & \frac{\partial -Im(\hat{\rho}(\omega_1))}{\partial g_1} & \cdots & \frac{\partial -Im(\hat{\rho}(\omega_1))}{\partial g_P}\\ \vdots & \ddots & & \vdots\\ \frac{\partial -Im(\hat{\rho}(\omega_m))}{\partial \rho_0} & \frac{\partial -Im(\hat{\rho}(\omega_m))}{\partial g_1} & \cdots & \frac{\partial -Im(\hat{\rho}(\omega_m))}{\partial g_P} \end{bmatrix}\\
  \Rightarrow \underline{\underline{J}}^{linear} &= \begin{bmatrix}\underline{\underline{J}}^{Re}_{linear}\\\underline{\underline{J}}^{-Im}_{linear}\end{bmatrix}

The Jacobian of :math:`\underline{f}^{log}` can now be computed using the chain rule:

.. math::

  \frac{\partial log_{10}(Z(Y))}{\partial Y} &= \frac{\partial log_{10}(Z)}{\partial Z} \cdot \frac{\partial Z}{\partial Y} = \frac{1}{Z \cdot log_e{10}} \cdot \frac{\partial Z}{\partial Y}\\
  \Rightarrow \underline{\underline{J}} &= \begin{bmatrix} \frac{\partial log_{10}(Re)(\hat{\rho}(\omega_1))}{\partial \rho_0} & \frac{\partial log_{10}(Re)(\hat{\rho}(\omega_1))}{\partial g_1} & \cdots & \frac{\partial log_{10}(Re)(\hat{\rho}(\omega_1))}{\partial g_P}\\ \vdots & \ddots & & \vdots\\ \frac{\partial log_{10}(Re)(\hat{\rho}(\omega_m))}{\partial \rho_0} & \frac{\partial log_{10}(Re)(\hat{\rho}(\omega_m))}{\partial g_1} & \cdots & \frac{\partial log_{10}(Re)(\hat{\rho}(\omega_m))}{\partial g_P} \\  \frac{\partial -Im(\hat{\rho}(\omega_1))}{\partial \rho_0} & \frac{\partial -Im(\hat{\rho}(\omega_1))}{\partial g_1} & \cdots & \frac{\partial -Im(\hat{\rho}(\omega_1))}{\partial g_P}\\ \vdots & \ddots & & \vdots\\ \frac{\partial -Im(\hat{\rho}(\omega_m))}{\partial \rho_0} & \frac{\partial -Im(\hat{\rho}(\omega_m))}{\partial g_1} & \cdots & \frac{\partial -Im(\hat{\rho}(\omega_m))}{\partial g_P} \end{bmatrix}\\
  &= \begin{bmatrix} \frac{1}{Re(\hat{\rho}(\omega_1)) log_e(10)} \cdot \frac{\partial Re(\hat{\rho})(\omega_1)}{\partial \rho_0} & \frac{1}{Re(\hat{\rho}(\omega_1)) log_e(10)} \cdot \frac{\partial Re(\hat{\rho}(\omega_1))}{\partial g_1} & \cdots & \frac{1}{Re(\hat{\rho}(\omega_1)) log_e(10)} \cdot\frac{\partial Re(\hat{\rho}(\omega_1))}{\partial g_P}\\ \vdots & \ddots & & \vdots\\  \frac{1}{Re(\hat{\rho}(\omega_K)) log_e(10)} \cdot \frac{\partial Re(\hat{\rho})(\omega_K)}{\partial \rho_0} & \frac{1}{Re(\hat{\rho}(\omega_K)) log_e(10)} \cdot \frac{\partial Re(\hat{\rho}(\omega_K))}{\partial g_1} & \cdots & \frac{1}{Re(\hat{\rho}(\omega_K)) log_e(10)} \cdot\frac{\partial Re(\hat{\rho}(\omega_K))}{\partial g_P}\\ \frac{\partial -Im(\hat{\rho})(\omega_1)}{\partial \rho_0} &  \frac{\partial -Im(\hat{\rho}(\omega_1))}{\partial g_1} & \cdots &  \frac{\partial -Im(\hat{\rho}(\omega_1))}{\partial g_P}\\ \vdots & \ddots & & \vdots\\  \frac{\partial -Im(\hat{\rho})(\omega_K)}{\partial \rho_0} & \frac{\partial -Im(\hat{\rho}(\omega_K))}{\partial g_1} & \cdots & \frac{\partial -Im(\hat{\rho}(\omega_K))}{\partial g_P}\end{bmatrix}\\

Debugging notes
===============

Random collection of notes:

* We have to save all inputs from the dicts in order to recreate an inversion
  (we need to reconstruct the whole inversion object for that). Therefore we
  should simplify the various dicts involved.

* For each iteration we want:

 * Sensitivities
 * Resolution matrix (covariance matrix)
 * Cumulative sensitivities
 * Data covariance matrix
 * Model covariance matrix


See also
========

.. toctree::

    dd_theory_eps
    dd_sensitivities
