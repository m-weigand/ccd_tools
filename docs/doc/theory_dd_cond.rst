Debye decomposition on conductivities
=====================================

complex
-------

After Tarasov and Titov, 2013:

.. math::

    \hat{\sigma}(\omega) &= \sigma_\infty \left(1 - \sum_i\frac{m_i}{1 + (j
    \omega \tau_i)}\right)\\
    m &= \frac{\sigma_\infty - \sigma_0}{\sigma_\infty}\\
    \sigma_0 &= (1 - m) \cdot \sigma_\infty\\
    \hat{\sigma}(\omega) &= \sigma_\infty \left[1  - \sum_k m_k
    \left[\frac{1}{1 + \omega^2 \tau_k^2} - j \frac{\omega \tau_k}{1 + \omega^2
    \tau_k^2} \right] \right]


real and imaginary parts
------------------------

.. math::

    \sigma'(\omega) &= \sigma_\infty \left[1 - \sum_k m_k \frac{1}{1 + \omega^2
    \tau_k^2}  \right] \\
    \sigma''(\omega) &= -\sigma_\infty \sum_k m_k \frac{\omega \tau_k}{1 +
    \omega^2 \tau_k^2}


derivatives
-----------

.. math::

    \frac{\partial \sigma'(\omega)}{\partial \sigma_\infty} &= 1 - \sum_k m_k
    \frac{1}{1 + \omega^2 \tau_k^2}\\
    \frac{\partial \sigma'(\omega)}{\partial m_k} &= - \sigma_\infty \frac{1}{1
    + \omega^2 \tau_k^2}\\
    \frac{\partial \sigma''(\omega)}{\partial \sigma_\infty} &= -\sum_k m_k
    \frac{\omega \tau_k}{1 + \omega^2 \tau_k^2}\\
    \frac{\partial \sigma''(\omega)}{\partial m_k} &= - \sigma_\infty
    \frac{\omega \tau_k}{1 + \omega^2 \tau_k^2}

