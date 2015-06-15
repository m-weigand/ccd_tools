Sensitivities
=============

Introduction
------------

The partial derivatives serve as sensitivitities:

.. math::

    \frac{\partial Re(\hat{\rho}(\omega))}{\partial \rho_0} &= 1 - \sum_{i=1}^N m_i \frac{(\omega 10^{s_i})^2}{1 + (\omega 10^{s_i})^2}\\
    \frac{\partial Re(\hat{\rho}(\omega))}{\partial mg_k} &= -\rho_0 \cdot \frac{(\omega 10^{s_k})^2}{1 + (\omega 10^{s_k})^2}\\
    \frac{\partial log_{10}(Re(\hat{\rho})(\omega))}{\partial \rho_0} &= \frac{1}{log_e{10}} \frac{\partial log_e(Re(\hat{\rho}))(\omega)}{\partial  \rho_0} = \frac{1}{log_e{10}} \frac{1}{Re(\hat{\rho})(\omega)} \frac{\partial Re(\hat{\rho}(\omega))}{\partial \rho_0}\\
    \frac{\partial log_{10}(Re(\hat{\rho})(\omega))}{\partial m_i} &= \frac{1}{log_e{10}} \frac{\partial log_e(Re(\hat{\rho}))(\omega)}{\partial m_i} = \frac{1}{log_e{10}} \frac{1}{Re(\hat{\rho})(\omega)} \frac{\partial Re(\hat{\rho}(\omega))}{\partial m_i}\\
    \frac{\partial -Im(\hat{\rho}(\omega))}{\partial \rho_0} &= \sum_{i=1}^N m_i \frac{(\omega 10^{s_i})}{1 + (\omega 10^{s_i})^2}\\
    \frac{\partial -Im(\hat{\rho}(\omega))}{\partial m_k} &= \rho_0 \cdot \frac{(\omega 10^{s_k})}{1 + (\omega 10^{s_k})^2}


:math:`Cov_f`
-------------

Coverage for each frequency: Sum up the sensitivitities of all m-Values for each frequency:

.. math::

    Cov^{Im}_f(f) = \sum_{i} \left( \frac{\partial[-Im(\hat{\rho}(\omega))]}{\partial m_i} \right)



:math:`Cov_m`
-------------

Coverage for each :math:`m` value: Sum up the sensitivities of all frequencies for each m-value:

.. math::

    Cov^{Im}_m(m_k) = \sum_{j} \left( \frac{[\partial -Im(\hat{\rho}(\omega_j))]}{\partial m_k} \right)


