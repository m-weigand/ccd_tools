Inversion and implementation details
====================================

.. toctree::

    starting_models

Normalisation
-------------

The DD is linear in :math:`\rho_0/\sigma_\infty`, as as such data can be
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

