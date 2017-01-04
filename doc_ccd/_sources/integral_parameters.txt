
.. _int_pars:

Integral Parameters
===================

*Integral parameters* extracted from the RTD fall into two categories:
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
  with the DC resistivity (Scott2003phd, Weller2010g_a). It gives an indication
  of the total polarization of the measured system without any influence of any
  occuring resistivity contrasts.

**Relaxation time parameters:**

Various parameters to determine characteristic relaxation times from the whole
RTD were proposed:

* Cumulative relaxation times :math:`\tau_x` denote relaxation times at which a
  certain percentage :math:`x` of chargeability is reached (Norsieg and Weller,
  2008; Zisser et al. 2010). For example, :math:`\tau_{50}` is the median
  relaxation time of a given RTD. (See ref:`environ_vars` on how to set
  individual percentages).
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

* Nordsiek et al., 2008 introduced the logarithmic average relaxation time
  :math:`\tau_{mean}`

  .. math::

      \tau_{mean} = \frac{exp(\sum_i m_i \cdot log(\tau_i))}{\sum m_i}`

The listed relaxation time parameters do not take into account the specific
shape of the RTD, and thus it is also useful to determine local maxima of the
distribution, e.g. to extract characteristic relaxation times specific to
certain polarisation peaks. This approach has conceptual similarities to the
use of (multi-)Cole-Cole models as the produced relaxation times can be
directly related to polarization peaks. The relaxation time with the larges
corresponding chargeability is called :math:`\tau_{max}`
(Attwa2013hess), and the in the generalized form the
relaxation time :math:`\tau_{peak}^i`, refers to the *i*-th local maximum of
the RTD, starting with the low frequencies (i.e. high :math:`\tau` values).
This approach can recover multiple peaks without any knowlegdge of the exact
number of peaks in the data.  However, this process can yield multiple small
maxima if the smoothing between adjacent chargeabilitiy values is not strong
enough. In these cases the corresponding smoothing parameters of the DD should
be increased.
*Integral parameters* extracted from the RTD fall into two categories:
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
  with the DC resistivity (Scott2003phd, Weller2010g_a). It gives an indication
  of the total polarization of the measured system without any influence of any
  occuring resistivity contrasts.

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

* Nordsiek et al., 2008 introduced the logarithmic average relaxation time
  :math:`\tau_{mean}`

  .. math::

      \tau_{mean} = \frac{exp(\sum_i m_i \cdot log(\tau_i))}{\sum m_i}`

The listed relaxation time parameters do not take into account the specific
shape of the RTD, and thus it is also useful to determine local maxima of the
distribution, e.g. to extract characteristic relaxation times specific to
certain polarisation peaks. This approach has conceptual similarities to the
use of (multi-)Cole-Cole models as the produced relaxation times can be
directly related to polarization peaks. The relaxation time with the larges
corresponding chargeability is called :math:`\tau_{max}`
(Attwa2013hess), and the in the generalized form the
relaxation time :math:`\tau_{peak}^i`, refers to the *i*-th local maximum of
the RTD, starting with the low frequencies (i.e. high :math:`\tau` values).
This approach can recover multiple peaks without any knowlegdge of the exact
number of peaks in the data.  However, this process can yield multiple small
maxima if the smoothing between adjacent chargeabilitiy values is not strong
enough. In these cases the corresponding smoothing parameters of the DD should
Integral Parameters
===================

*Integral parameters* extracted from the RTD fall into two categories:
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
  with the DC resistivity (Scott2003phd, Weller2010g_a). It gives an indication
  of the total polarization of the measured system without any influence of any
  occuring resistivity contrasts.

**Relaxation time parameters:**

Various parameters to determine characteristic relaxation times from the whole
RTD were proposed:

* Cumulative relaxation times :math:`\tau_x` denote relaxation times at which a
  certain percentage :math:`x` of chargeability is reached (Norsieg and Weller,
  2008; Zisser et al. 2010). For example, :math:`\tau_{50}` is the median
  relaxation time of a given RTD. (See ref:`environ_vars` on how to set
  individual percentages).
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

* Nordsiek et al., 2008 introduced the logarithmic average relaxation time
  :math:`\tau_{mean}`

  .. math::

      \tau_{mean} = \frac{exp(\sum_i m_i \cdot log(\tau_i))}{\sum m_i}`

The listed relaxation time parameters do not take into account the specific
shape of the RTD, and thus it is also useful to determine local maxima of the
distribution, e.g. to extract characteristic relaxation times specific to
certain polarisation peaks. This approach has conceptual similarities to the
use of (multi-)Cole-Cole models as the produced relaxation times can be
directly related to polarization peaks. The relaxation time with the larges
corresponding chargeability is called :math:`\tau_{max}`
(Attwa2013hess), and the in the generalized form the
relaxation time :math:`\tau_{peak}^i`, refers to the *i*-th local maximum of
the RTD, starting with the low frequencies (i.e. high :math:`\tau` values).
This approach can recover multiple peaks without any knowlegdge of the exact
number of peaks in the data.  However, this process can yield multiple small
maxima if the smoothing between adjacent chargeabilitiy values is not strong
enough. In these cases the corresponding smoothing parameters of the DD should
be increased.
*Integral parameters* extracted from the RTD fall into two categories:
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
  with the DC resistivity (Scott2003phd, Weller2010g_a). It gives an indication
  of the total polarization of the measured system without any influence of any
  occuring resistivity contrasts.

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

* Nordsiek et al., 2008 introduced the logarithmic average relaxation time
  :math:`\tau_{mean}`

  .. math::

      \tau_{mean} = \frac{exp(\sum_i m_i \cdot log(\tau_i))}{\sum m_i}`

The listed relaxation time parameters do not take into account the specific
shape of the RTD, and thus it is also useful to determine local maxima of the
distribution, e.g. to extract characteristic relaxation times specific to
certain polarisation peaks. This approach has conceptual similarities to the
use of (multi-)Cole-Cole models as the produced relaxation times can be
directly related to polarization peaks. The relaxation time with the larges
corresponding chargeability is called :math:`\tau_{max}`
(Attwa2013hess), and the in the generalized form the
relaxation time :math:`\tau_{peak}^i`, refers to the *i*-th local maximum of
the RTD, starting with the low frequencies (i.e. high :math:`\tau` values).
This approach can recover multiple peaks without any knowlegdge of the exact
number of peaks in the data.  However, this process can yield multiple small
maxima if the smoothing between adjacent chargeabilitiy values is not strong
enough. In these cases the corresponding smoothing parameters of the DD should
Integral Parameters
===================

*Integral parameters* extracted from the RTD fall into two categories:
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
  with the DC resistivity (Scott2003phd, Weller2010g_a). It gives an indication
  of the total polarization of the measured system without any influence of any
  occuring resistivity contrasts.

**Relaxation time parameters:**

Various parameters to determine characteristic relaxation times from the whole
RTD were proposed:

* Cumulative relaxation times :math:`\tau_x` denote relaxation times at which a
  certain percentage :math:`x` of chargeability is reached (Norsieg and Weller,
  2008; Zisser et al. 2010). For example, :math:`\tau_{50}` is the median
  relaxation time of a given RTD. (See ref:`environ_vars` on how to set
  individual percentages).
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

* Nordsiek et al., 2008 introduced the logarithmic average relaxation time
  :math:`\tau_{mean}`

  .. math::

      \tau_{mean} = \frac{exp(\sum_i m_i \cdot log(\tau_i))}{\sum m_i}`

The listed relaxation time parameters do not take into account the specific
shape of the RTD, and thus it is also useful to determine local maxima of the
distribution, e.g. to extract characteristic relaxation times specific to
certain polarisation peaks. This approach has conceptual similarities to the
use of (multi-)Cole-Cole models as the produced relaxation times can be
directly related to polarization peaks. The relaxation time with the larges
corresponding chargeability is called :math:`\tau_{max}`
(Attwa2013hess), and the in the generalized form the
relaxation time :math:`\tau_{peak}^i`, refers to the *i*-th local maximum of
the RTD, starting with the low frequencies (i.e. high :math:`\tau` values).
This approach can recover multiple peaks without any knowlegdge of the exact
number of peaks in the data.  However, this process can yield multiple small
maxima if the smoothing between adjacent chargeabilitiy values is not strong
enough. In these cases the corresponding smoothing parameters of the DD should
be increased.
*Integral parameters* extracted from the RTD fall into two categories:
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
  with the DC resistivity (Scott2003phd, Weller2010g_a). It gives an indication
  of the total polarization of the measured system without any influence of any
  occuring resistivity contrasts.

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

* Nordsiek et al., 2008 introduced the logarithmic average relaxation time
  :math:`\tau_{mean}`

  .. math::

      \tau_{mean} = \frac{exp(\sum_i m_i \cdot log(\tau_i))}{\sum m_i}`

The listed relaxation time parameters do not take into account the specific
shape of the RTD, and thus it is also useful to determine local maxima of the
distribution, e.g. to extract characteristic relaxation times specific to
certain polarisation peaks. This approach has conceptual similarities to the
use of (multi-)Cole-Cole models as the produced relaxation times can be
directly related to polarization peaks. The relaxation time with the larges
corresponding chargeability is called :math:`\tau_{max}`
(Attwa2013hess), and the in the generalized form the
relaxation time :math:`\tau_{peak}^i`, refers to the *i*-th local maximum of
the RTD, starting with the low frequencies (i.e. high :math:`\tau` values).
This approach can recover multiple peaks without any knowlegdge of the exact
number of peaks in the data.  However, this process can yield multiple small
maxima if the smoothing between adjacent chargeabilitiy values is not strong
enough. In these cases the corresponding smoothing parameters of the DD should
be increased.
