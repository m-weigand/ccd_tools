Mathematical helper terms
=========================

The following expressions are used in the following presentation of the various
model equations:

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


.. math::

    \frac{\partial}{\partial c} (\omega \tau)^c &= \frac{\partial}{\partial c}
    e^{\ln (\omega \tau)^c} = \frac{\partial e^{c \ln (\omega \tau)}}{\partial
    c} = \ln (\omega \tau) \cdot e^{c \ln (\omega \tau)} = \ln (\omega \tau)
    (\omega \tau)^c\\
    \frac{\partial (\omega \tau)^{2 c}}{\partial c} &= 2 \ln (\omega \tau)
    (\omega \tau)^{2 c}\\
    \frac{\partial}{\partial c} \left[(\omega \tau)^{c} \sin \frac{c \pi}{2}\right] &= \ln (\omega \tau) (\omega
    \tau)^c \sin \frac{c \pi}{2} + (\omega \tau)^c \cos \left(\frac{c \pi}{2}\right)
    \frac{\pi}{2}\\
    \frac{\partial}{\partial c} \left[2 (\omega \tau)^c \cos \frac{c \pi}{2} \right] &=
    2 \ln(\omega \tau) (\omega \tau)^c \cos \frac{c \pi}{2} - 2 (\omega \tau)^c \frac{\pi}{2} \sin \frac{c \pi}{2}


.. math::

    \frac{\partial}{\partial c} (\omega \tau)^c &= c \omega (\omega \tau)^{c - 1}\\
    \frac{\partial}{\partial c} \left[ 1 + 2 (\omega \tau)^c \cos \frac{c \pi}{2} + (\omega \tau)^{2 c} \right] &=
    2 c \omega (\omega \tau)^{c -1} \cos \frac{c \pi}{2} + 2 c (\omega \tau)^{2
    c - 1} \omega

Partial derivatives respect to :math:`log_{10}(x)`:

.. math::

    \frac{\partial y}{\partial x} &= \frac{\partial y}{\partial u} \cdot \frac{\partial u}{\partial x}\\
    \frac{\partial F(X)}{\partial x} &= \frac{\partial F(X)}{\partial log_{10}(x)} \cdot \frac{\partial log_{10}(x)}{\partial x}\\
    \frac{\partial F(X)}{\partial x} &= \frac{\partial F(X)}{\partial log_{10}(x)} \cdot \frac{1}{x \cdot log(x)}\\
    \Rightarrow \frac{\partial F(X)}{\partial log_{10}(x)} &= \frac{\partial F(X)}{\partial x} \cdot x \cdot log(x)

Remember:

* :math:`\frac{\partial}{\partial x} \cdot 10^x = log_e(10) 10^x`
* :math:`log_{10}(F(x)) = \frac{log_e(F(x))}{log_e(10)}`
* :math:`\frac{\partial}{\partial x} log_{10}(F(x)) = \frac{1}{log_e(10)} \cdot
  \frac{1}{F(x)} \cdot \frac{\partial F(x)}{\partial x}`

.. math::

    \frac{\partial F(x)}{\partial \log_{10}(x)} &= \\
    \frac{\partial log_{10}(F(x))}{\partial x} &= \\
    \frac{\partial log_{10}(F(x))}{\partial \log_{10}(x)} &= \\


