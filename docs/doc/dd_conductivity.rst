Formulation in conductivities
-----------------------------

After Tarasov and Titov, 2013:

.. math::

    \hat{\sigma}(\omega) &= \sigma_\infty \left(1 - \sum_i\frac{m_i}{1 + (j \omega \tau_i)}\right)\\
    m &= \frac{\sigma_\infty - \sigma_0}{\sigma_\infty}\\
    \sigma_0 &= (1 - m) \cdot \sigma_\infty\\
    \hat{\sigma}(\omega) &= \sigma_\infty \left[1  - \sum_i m_i \left[\frac{1}{1 + \omega^2 \tau_i^2} - i \frac{\omega \tau_i}{1 + \omega^2 \tau_i^2} \right] \right]


Peak relaxation times
---------------------

Peak relaxation times for the conductivity (a.k.a. Cole-Cole, CC) and the
resistivity (a.k.a. Pelton, P) formulation are related by:

.. math::

    \tau_{CC} &= (1 - m)^{\frac{1}{c}} \tau_P\\
    \text{Peak frequencies for the imaginary parts then are related by:}\\
    \tau_{P}^{peak} = \frac{1}{\omega_{P}^{peak}}\\
    \tau_{CC}^{peak} = \frac{1}{\omega_{CC}^{peak}}\\
    \omega_{CC} = (1 - m)^{-\frac{1}{c}} \omega_{P}

The relation hold for both the Cole-Cole model and the Debye model (c=1).
Additionally, they also hold for the decomposition approach, here the
chargeability has to be replaced by the total chargeability: :math:`m
\rightarrow \sum_i m_i`.
