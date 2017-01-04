Starting Models
---------------

The following methods can be used to determine starting models. A specific
method can be selected by setting the environment variable
**DD_STARTING_MODEL** to the corresponding integer number, i.e.:

::

    DD_STARTING_MODEL=3 dd_single.py ...

* (`DD_STARTING_MODEL = 1`): Flat starting model
* (`DD_STARTING_MODEL = 2`): [TODO] (Gaussian, center at peak of imaginary part)
* (`DD_STARTING_MODEL = 3`): [TODO] (Frequency decade wise approximation)

This page describes the implemented starting models

Model 1
^^^^^^^

Model 2
^^^^^^^

Model 3
^^^^^^^

This starting model heuristic implements the following procedure:

* Compute mean values for :math:`\rho''` for each data frequency decade.
* Compute mean log10 relaxation times for each relaxation time decade.
* Now compute a constant chargeability value for each frequency decade:

  .. math::

    \rho'' = - \rho_0 \sum_i m_i \frac{\omega \tau_i}{1 + (\omega \tau)^2}\\
    \Rightarrow\\
    \rho'' = - \rho_0 \overline{m} \sum_i \frac{\omega \tau_i}{1 + (\omega \tau_i)^2}\\
    \overline{m} = -\frac{\rho''}{\rho_0} \left[ \sum_i \frac{\omega \tau_i}{1
    + (\omega \tau_i)^2} \right]^{-1}

* Use this chargeability value for the relaxation times related to each frequency decade
* Norm the chargeabilities to 1
* Sample the :math:`RMS_{Im}` values for scaling factors between 0 and 1
* Choose the value with the lowest rms and take the entries next to it (on the
  scaling factor axis). Then fit a parabola through these three (scale, rms)
  points and determine the minimum of this parabola. Take this minium as the
  final scaling factor. Use 1 as an upper maximum, and a really small value
  above zero as a lower value.

