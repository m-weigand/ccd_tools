Inversion
=========

Misfit function
---------------

The basic aim is to minimize the misfit function, which consists of an data
misfit term :math:`\Psi_d` and a model misfit term :math:`\Psi_m`. The data
misfit term is the quadratic misfit between data values and model response. The
model misfit term is usually used to minimize certain constraints (i.e.
regularizations), but also serves to stablize the optimization problem (prevent
matrices from getting singular). The regularization is formulated for multiple
regularization functions with individual regularization parmeters.

The whole misfit function thus formulates as follows:

.. math::

    \Psi &= \Psi_d + \Psi_m\\
    \Psi &= \left|\left|\sum_i^N\frac{d_i - f_i(\underline{m}}
        {\epsilon_i}\right|\right|^2 + \sum_i \lambda_i \Psi_{m, i}

Each of the model misfit terms can have a multitude of realizations. Three
common use cases (Tikhonov regularization zeroth, first, and second order) are:

.. math::

    \Psi^0_m & = \left|\left|\underline{m}\right|\right|^2\\
    \Psi^1_m &= \left|\left|\nabla\underline{m}\right|\right|^2\\
    \Psi^2_m &= \left|\left|\nabla^2\underline{m}\right|\right|^2

For a detailed introduction, see for example Aster, page 98+.

The model misfit functions described above can be formulated in a matrix
formulation using a discrete approximation of the :math:`\nabla` operator:

.. math::

    &\int ||\nabla \underline{m}||^2 d\tau \rightarrow \sum_{i=1}^{Z-1}
    \left|\left| \frac{\partial \underline{m}}{\partial \tau_i}
    \right|\right|^2 \nabla \tau_i \\
    &= \sum_{i=1}^{z-1} \left|\left| \frac{\nabla \underline{m}}{\nabla \tau_i}
    \right|\right| \nabla \tau_i  = \sum_{i=1}^{z-1} \left( \frac{g_{i+1} -
    g_i}{\tau_{i+1} - \tau_i} \right)^2 (\tau_{i+1} - \tau_i) =
    \sum_{i=1}^{Z-1} \left( \frac{1}{\sqrt{\tau_{i+1} - \tau_i}} (g_{i+1} -
    g_i) \right)\\
    &\Leftrightarrow \underline{m}^T \underline{\underline{R}}^T
    \underline{\underline{R}} \underline{m} = (\underline{\underline{R}}
    \underline{m})^2 = \sum_{i=1}^{Z-1}(\underline{\underline{R}}_{ij} \cdot
    g_i)\\
    &\Rightarrow (\underline{\underline{R}} \underline{m})_k =
    \frac{1}{\sqrt{\tau_{k+1} - \tau_k}} \cdot (-1 \cdot g_k + 1 \cdot
    g_{k+1})\\
    &\Rightarrow \underline{\underline{R}}_{normed} = \begin{bmatrix} -1 & 1 &
    0 & \cdots & 0\\ 0 & \ddots & \ddots & \ddots & 0\\  \ddots & 0 & -1 & 1 &
    0\\\ddots & \ddots & 0 & -1& 1 \end{bmatrix}\\
    \Rightarrow \Psi_m^1 &= \underline{m}^T \underline{\underline{R}}^T \cdot
    \underline{\underline{R}} \underline{m}

* TODO 0: Shouldn't we either go from 0 to z-1 or from 1 to z?

* TODO1: Why do we use the left neighbour of each parameter, not the right? Does
         this matter or are both variants equivalent?

In a similar matter it follows for a second order smoothing:

.. math::

    \underline{\underline{R_2}} = \begin{bmatrix} 1 & -2 & 1 & 0 & \cdots & 0 \\
    0 & 1 & -2 & 1 & 0 & \cdots\\ \ddots & \ddots & \ddots &  \ddots & \ddots &
    \ddots \\0 & 0 & 0 & 1 & -2 &  1 \end{bmatrix}

Note that second order smoothing in general implies a regular distance between
the parameters (e.g. frequencies or times) due to the finite-difference
approximation. This also prevents the application of a distance-based weighting
for the regularization for a second order smoothing.

.. math::

    \frac{\partial f}{\partial x} = lim_{h \rightarrow 0} \frac{f(x + h) - f(x)}{h}
    \frac{\partial^2 f}{\partial x^2} = lim_{h \rightarrow 0} \frac{f(x + 2h) - 2 f(x+h) + f(x)}{h^2}

Time-based weighting
~~~~~~~~~~~~~~~~~~~~

The first order smoothing can be weighted according to the time-difference
between measurements. In fact, this is the direct implementation of the
finite-difference approximation of the derivative operator, :math:`h` being the
time distance between any two timesteps.

In practice this time difference can be included by multiplying each line of
:math:`\underline{\underline{W}}_m` with the difference to the next time step
(see Günther Diss):

.. math::

    \underline{\underline{W}}_m^{time weighted} &= \underline{\underline{W}}_{time~weighting} \cdot \underline{\underline{W}}_m\\
    &\text{with:}\\
    \underline{\underline{W}}_{time~weighting} &= \begin{pmatrix}\frac{1}{\Delta t_{1,2}} & \cdots &  & \\ \cdots & \frac{1}{\Delta t_{2,3}} & \cdots & \\ \cdots & \ddots & \ddots & \cdots \\ & & & \frac{1}{\Delta t_{n-1, n}}\end{pmatrix}\\
    \underline{\underline{W}}_{time~weighting} &: (N-1) x (N-1)



Disconnecting certain cells in the regularization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes certain parameter should not be regularized (e.g. in the Debye
decomposition we have :math:`\rho_0` as the first entry of
:math:`\underline{m}` and do not want to regularize :math:`\rho_0` against the
chargeability values.) Thus the regularization matrix transforms to:

.. math::

    \Rightarrow \underline{\underline{R}}'_{normed} = \begin{bmatrix} 0 & 0 \\
    0 & \underline{\underline{R}}_{normed} \end{bmatrix}

:math:`\Rightarrow \underline{\underline{R}}'_{normed}` is a P-1 x P matrix,
with P the number of model parameters (1 + number of chargeabilities/relaxation
times).

Inversion of multi-dimensional data
-----------------------------------

The inversion problem formulated above can directly be used for the inversion
of multi-dimensional data. This is best described using a small example:

Given D complex resistivity spectra :math:`\rho(\omega) = \rho'(\omega) + i
\cdot \rho''(\omega)` for F frequencies. We want to fit these D spectra to a
model which takes M parameters as an input and puts out one complex resistivity
spectrum. The model space we seek is thus MxD (one parameter set for each
spectrum). On the other hand we have a Fx2xD data space (for each frequency
there are two different values :math:`\sigma'` and :math:`\sigma''`, and D
spectra.

If we now collapse the data and the model space to the vectors:

.. math::

   \underline{d}_{all} &= \begin{pmatrix}
        \left. \begin{pmatrix} \rho'(\omega_1)\\ \vdots \\ \rho'(\omega_F)\\
        \rho''(\omega_1)\\ \vdots \\ \rho''(\omega_F) \end{pmatrix} \right\}
        d=1\\
        \vdots\\
        \left. \begin{pmatrix} \rho'(\omega_1)\\ \vdots \\ \rho'(\omega_F)\\
        \rho''(\omega_1)\\ \vdots \\ \rho''(\omega_F) \end{pmatrix} \right\}
        d=D\\
    \end{pmatrix}\\
    \underline{f}_{all} &= \begin{pmatrix}
     \left. \begin{pmatrix} \rho_0\\ m\\ \tau\\ c\end{pmatrix}\right\} d=1\\
     \vdots\\
     \left. \begin{pmatrix} \rho_0\\ m\\ \tau\\ c\end{pmatrix}\right\} d=D\\
     \end{pmatrix}

The corresponding Jacobian matrix can easily be assembled from the Jacobians
for each parameter set:

.. math::

    \underline{\underline{J}}_{all} &= \begin{bmatrix}
    \underline{\underline{J}}_{d=1} & 0 & \hdots\\ 0 &
    \underline{\underline{J}}_{d=2}\\ \ddots & \ddots & \ddots\\ 0 & 0 &
    \underline{\underline{J}}_{d=D}\end{bmatrix}

with:

.. math::

    \underline{\underline{J}}_{d=1} =
    \begin{bmatrix}\underline{\underline{J_{\rho'}}}\\
    \underline{\underline{J_{\rho''}}}\end{bmatrix}

:math:`\underline{\underline{J}}_{d=1}` has the size (2F x M). Therefore,
\underline{\underline{J}}_{all} has the the size :math:`(M \cdot D) x (2F
\cdot D)`.

Model update
------------

The model update for the one or multi-dimensional inversion step can now be
formulated as follows:

.. math::

    \underline{m}_{q+1} &= \underline{m}_q + \bigtriangleup \underline{m}_q\\
    &\text{or}\\
    \underline{m}_{q+1} &= \underline{m}_q + \alpha \bigtriangleup
    \underline{m}_q \quad \text{with } \alpha \text{ the steplength}\\
    \Psi(\underline{m}_{q+1}) &= ||\underline{d} -
    \underline{f}(\underline{m}_{q+1})||^2 + \sum_i \lambda_i
    ||\underline{\underline{W}}_{m,i} \underline{m}_q||^2\\
    \Rightarrow \bigtriangleup \underline{m}_q &=
    \left[\underline{\underline{J}}_q^T \underline{\underline{J}} + \sum_i \lambda_i
    \underline{\underline{W}}_{m,i}^T \underline{\underline{W}}_{m,i} \right]^{-1}\left[
    \underline{\underline{J}}_q^T (\underline{d} -
    \underline{f}(\underline{m}_{q}))  - \sum_i \lambda_i \underline{\underline{W}}_{m,i}^T
    \underline{\underline{W}}_{m,i} \underline{m}_q \right]\\
    &\text{including weighting}\\
    \Rightarrow \bigtriangleup \underline{m}_q &=
    \left[\underline{\underline{J}}_q^T \underline{\underline{W}}_d^T
    \underline{\underline{W}}_d \underline{\underline{J}} + \sum_i \lambda_i
    \underline{\underline{W}}_{m,i}^T \underline{\underline{W}}_{m,i}\right]^{-1} \left[
    \underline{\underline{J}}_q^T \underline{\underline{W}}_d^T
    \underline{\underline{W}}_d (\underline{d} -
    \underline{f}(\underline{m}_{q}))  - \sum_i \lambda_i \underline{\underline{W}}_{m,i}^T
    \underline{\underline{W}}_{m,i} \underline{m}_q \right]\\

If individual :math:`\lambda` values are used for multiple spectra, then
:math:`\lambda` transforms to a diagonal matrix
:math:`\underline{\underline{L}}`:

.. math::

    \underline{\underline{L}} = \begin{pmatrix}\lambda_1 & 0 & \hdots & 0 \\ 0 & \lambda_2 & 0 & \hdots \\ 0 & \hdots & \ddots & 0\\ 0 & \hdots & 0 & \lambda_N \end{pmatrix}

For a time-based weighting, :math:`\underline{\underline{W}}_{m,i}` becomes
:math:`\underline{\underline{T}}_{m,i} \cdot \underline{\underline{W}}_{m,i}`,
where :math:`\underline{\underline{T}}_{m,i}` is a (N-1) x (N-1) diagonal
matrix:

.. math::

    \underline{\underline{T}}_{m,i} = \begin{pmatrix}\frac{1}{\Delta t_{1,2}} & 0 & \hdots & 0 \\ 0 & \frac{1}{\Delta t_{2,3}} & 0 & \hdots \\ 0 & \hdots & \ddots & 0\\ 0 & \hdots & 0 & \frac{1}{\Delta t_{N-1,N}} \end{pmatrix}

Steplength selection
--------------------

To prevent overshooting during an iteration update, a simple line search is
conducted before each model update to determine an optimal steplength
:math:`\alpha`. Here a parabola is fitted to to the three :math:`\alpha` values
0, 0.5 and 1, and the minimum of this parabola is then used as the steplength
for the model update. In the case of the minimum being located above 1, the
steplength will be set to 1. For :math:`\alpha_{min} \leq 0`, a hardcoded value
of :math:`\alpha = 0.1` is returned. Note that in this case the model update
leads to an increase in the RMS values and the inversion will be cancled before
this update is applied.

See also Günther, 2004, PhD, page 83.

:math:`\lambda` selection
-------------------------

TODO
