Formulation using the dielectric constant :math:`\epsilon`
==========================================================

Böttcher and Bordewijk, page 40:

.. math::

    \hat{\epsilon}(\omega) &= \epsilon_\infty + (\epsilon - \epsilon_\infty) \int_0^\infty \frac{g(\tau)}{1 + i \omega \tau} d\tau\\
    &\text{with}\\
    &\int_0^\infty g(\tau) d\tau = 1


For a :math:`g(\tau) = \delta(\tau - \tau_1)` it follows (see eqs. 8.182 in B&B):

.. math::

   \hat{\epsilon}(\omega) &= \epsilon_\infty + (\epsilon - \epsilon_\infty) \frac{g(\tau)}{1 + i \omega \tau_1}

For multiple relaxation times in a discrete case (8.187 in B&W):

.. math::

    \hat{\epsilon}(\omega) &= \epsilon_\infty + (\epsilon - \epsilon_\infty) \sum_k \frac{g_k}{1 + i \omega \tau_k}\\
    &\text{with}\\
    &\sum_k g_k = 1

Transformation to conductivity
------------------------------

Tarasov and Titov substitute :math:`\epsilon` for :math:`\sigma` (they cite the electrostatic analogy and the formulation for dielectric materials with losses):

.. math::

    \hat{\sigma}(\omega) &= \sigma_\infty + (\sigma - \sigma_\infty) \int_0^{\infty} \frac{g(\tau)}{1 + i \omega \tau} d\tau\\
    &\text{with}:\\
    &\int_0^{\infty} g(\tau) d\tau
  
