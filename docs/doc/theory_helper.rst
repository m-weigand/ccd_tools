Mathematical helper terms
=========================

.. math::

    j &= e^{j \frac{\pi}{2}}\\
    \Rightarrow j^c &= \left(e^{j \frac{\pi}{2}} \right)^c\\
    &= e^{j \frac{c \pi}{2}}\\
    &= \cos\left(\frac{c \pi}{2}\right) + j \sin{\left(\frac{c \pi}{2}\right)}

.. math::

    \frac{1}{1 + (j \omega \tau)^c} &= \frac{1}{1 + \cos\left(\frac{c
    \pi}{2}\right) + j \sin \left(\frac{c \pi}{2}\right)}\\
    &= \frac{1 + (\omega \tau)^c \cos \left(\frac{c \pi}{2}\right) - j (\omega
    \tau)^c \sin\left( \frac{c \pi}{2}\right)}{\left[1 + (\omega \tau)^c \cos
    \left(\frac{c \pi}{2}\right) + j (\omega \tau)^c \sin\left( \frac{c
    \pi}{2}\right) \right] \cdot \left[1 + (\omega \tau)^c \cos \left(\frac{c
    \pi}{2}\right) - j (\omega \tau)^c \sin\left( \frac{c \pi}{2}\right)
    \right]}\\
    &= \frac{1 + (\omega \tau)^c \cos \left(\frac{c \pi}{2}\right) - j (\omega
    \tau)^c \sin\left( \frac{c \pi}{2}\right)}{\left[1 + (\omega \tau)^c
    \cos\left(\frac{c \pi}{2}\right) \right]^2 + \left[(\omega \tau)^c
    \sin\left( \frac{c \pi}{2}\right) \right]^2}\\
    &= \frac{1 + (\omega \tau)^c \cos \left(\frac{c \pi}{2}\right) - j (\omega
    \tau)^c \sin\left( \frac{c \pi}{2}\right)}{1 + 2 (\omega \tau)^c \cos
    \left(\frac{c \pi}{2}\right) + (\omega \tau)^{2c}}




