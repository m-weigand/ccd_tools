Cole-Cole decomposition conductivities
======================================

complex
-------
After Tarasov and Titov, 2013:


.. math::

    \hat{\sigma}(\omega) &= \sigma_\infty \left(1 - \sum_k\frac{m_k}{1 + (j
    \omega \tau_k)^c}\right)\\
    &= \sigma_\infty \left( 1 - \sum_k m_k \frac{1 + (\omega \tau)^c \cos
    \frac{c \pi}{2} - j (\omega \tau)^c \sin \frac{c \pi}{2}}{1 + 2 (\omega
    \tau)^c \cos \frac{c \pi}{2} + (\omega \tau)^{2 c}} \right)\\
    &= \sigma_\infty \left( 1 - \sum_k m_k \frac{1 + (\omega \tau)^c \cos
    \frac{c \pi}{2}}{1 + 2 (\omega
    \tau)^c \cos \frac{c \pi}{2} + (\omega \tau)^{2 c}} \right) +
    j \sigma_\infty \sum_k m_k  \frac{(\omega \tau)^c \sin \frac{c \pi}{2}}{1 + 2 (\omega
    \tau)^c \cos \frac{c \pi}{2} + (\omega \tau)^{2 c}}\\
    \Rightarrow \sigma' &=  \sigma_\infty \left( 1 - \sum_k m_k \frac{1 +
    (\omega \tau)^c \cos \frac{c \pi}{2}}{1 + 2 (\omega \tau)^c \cos \frac{c
    \pi}{2} + (\omega \tau)^{2 c}} \right)\\
    \sigma'' &=     j \sigma_\infty \sum_k m_k  \frac{(\omega \tau)^c \sin
    \frac{c \pi}{2}}{1 + 2 (\omega \tau)^c \cos \frac{c \pi}{2} + (\omega
    \tau)^{2 c}}\\
    m &= \frac{\sigma_\infty - \sigma_0}{\sigma_\infty}\\
    \sigma_0 &= (1 - m) \cdot \sigma_\infty


derivatives
-----------

.. math::

    \frac{\partial \hat{\sigma'}(\omega)}{\partial \sigma_\infty} &= 1 - \sum_k m_k \frac{1 +
    (\omega \tau)^c \cos \frac{c \pi}{2}}{1 + 2 (\omega \tau)^c \cos \frac{c
    \pi}{2} + (\omega \tau)^{2 c}}\\
    \frac{\partial \hat{\sigma'}(\omega)}{\partial m_i} &= -\sigma_\infty \frac{1 +
    (\omega \tau)^c \cos \frac{c \pi}{2}}{1 + 2 (\omega \tau)^c \cos \frac{c
    \pi}{2} + (\omega \tau)^{2 c}}\\
    \frac{\partial \hat{\sigma'}(\omega)}{\partial \tau_k} &=  \\
    \frac{\partial \hat{\sigma'}(\omega)}{\partial c} &= 

.. math::

    \frac{\partial \hat{\sigma}''(\omega)}{\partial \sigma_\infty} &= - \frac{m (\omega
    \tau)^c \sin(\frac{c \pi}{2})}{1 + 2 (\omega \tau)^c \cos(\frac{c \pi}{2}) +
    (\omega \tau)^{2 c}}\\
    \frac{\partial \hat{\sigma''}(\omega)}{\partial m} &= - \sigma_\infty m (\omega
    \tau)^c \frac{sin(\frac{c \pi}{2})}{1 + 2 (\omega \tau)^c \cos(\frac{c
    \pi}{2}) + (\omega \tau)^{2 c}}\\
    \frac{\partial \hat{\sigma''}(\omega)}{\partial \tau} &= \sigma_\infty \frac{-m
    \omega^c c \tau^{c-1} \sin(\frac{c \pi}{2} }{1 + 2 (\omega \tau)^c
    \cos(\frac{c \pi}{2}) + (\omega \tau)^{2 c}} +\\
    &\sigma_0 \frac{\left[-m (\omega
    \tau)^c \sin(\frac{c \pi}{2} \right] \cdot \left[ 2 \omega^c c \tau^{c-1}
    \cos(\frac{c \pi}{2}) + 2 c \omega^{2 c} \tau^{2 c - 1}\right]}{\left[1 + 2
    (\omega \tau)^c \cos(\frac{c \pi}{2}) + (\omega \tau)^{2 c}\right]^2}\\
    \frac{\partial \hat{\sigma''}(\omega)}{\partial c} &= \sigma_0 \frac{-m
    \sin(\frac{c \pi}{2}) \ln(\omega \tau)(\omega \tau)^c - m (\omega \tau)^c
    \frac{\pi}{2} \cos(\frac{\pi}{2}}{1 + 2 (\omega \tau)^c \cos(\frac{c \pi}{2})
    + (\omega \tau)^{2 c}} +\\
     &\sigma_0 \frac{\left[-m (\omega \tau)^c \cos(\frac{c
      \pi}{2}) \right] \cdot \left[ -2 \ln(\omega \tau) (\omega \tau)^c
      \cos(\frac{c \pi}{2}) + 2 (\omega \tau)^c \frac{\pi}{2} \cos(\frac{c
      \pi}{2}) \right] + \left[2 \ln(\omega \tau) (\omega \tau)^{2
      c}\right]}{\left[1 + 2 (\omega \tau)^c \cos(\frac{c \pi}{2}) + (\omega
      \tau)^{2 c}\right]^2}
