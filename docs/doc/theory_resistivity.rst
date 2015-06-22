
Formulation in resistivities
============================

Formulation linear in rho and mi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::

  \hat{\rho}(\omega) &= \rho_0 \left(1 - \sum_{i=1}^{N} m_k \left[1 -
  \frac{1}{1 + i \omega \tau_i}\right] \right)\\
  &= \rho_0 \left[ 1 - \sum_{i=1}^{N} m_k \left(\frac{(\omega \tau_k)^2}{1 +
  (\omega \tau_i)^2} + i \frac{\omega \tau_i}{1 + (\omega \tau_i)^2}
  \right)\right]\\
 \Rightarrow Re(\hat{\rho}(\omega)) &= \rho_0 -  \rho_0 \sum_{i=1}^N m_i
 \frac{(\omega \tau_i)^2}{1 + (\omega \tau_i)^2}\\
 \Rightarrow Im(\hat{\rho}(\omega)) &= -  \rho_0 \sum_{i=1}^N m_i \frac{(\omega
 \tau_k)}{1 + (\omega \tau_k)^2}

Substitute :math:`s_i = log_{10}(\tau_i) \Leftrightarrow \tau_i = 10^{s_i}`

.. math::

    \Rightarrow Re(\hat{\rho}(\omega)) &= \rho_0 -  \rho_0 \sum_{i=1}^N m_i \frac{(\omega 10^{s_i})^2}{1 + (\omega 10^{s_i})^2}\\
    \Rightarrow -Im(\hat{\rho}(\omega)) &= \rho_0 \sum_{i=1}^N m_i \frac{(\omega 10^{s_i})}{1 + (\omega 10^{s_i})^2}\\
    \frac{\partial Re(\hat{\rho}(\omega))}{\partial \rho_0} &= 1 - \sum_{i=1}^N m_i \frac{(\omega 10^{s_i})^2}{1 + (\omega 10^{s_i})^2}\\
    \frac{\partial Re(\hat{\rho}(\omega))}{\partial mg_k} &= -\rho_0 \cdot \frac{(\omega 10^{s_k})^2}{1 + (\omega 10^{s_k})^2}\\
    \frac{\partial log_{10}(Re(\hat{\rho})(\omega))}{\partial \rho_0} &= \frac{1}{log_e{10}} \frac{\partial log_e(Re(\hat{\rho}))(\omega)}{\partial  \rho_0} = \frac{1}{log_e{10}} \frac{1}{Re(\hat{\rho})(\omega)} \frac{\partial Re(\hat{\rho}(\omega))}{\partial \rho_0}\\
    \frac{\partial log_{10}(Re(\hat{\rho})(\omega))}{\partial m_i} &= \frac{1}{log_e{10}} \frac{\partial log_e(Re(\hat{\rho}))(\omega)}{\partial m_i} = \frac{1}{log_e{10}} \frac{1}{Re(\hat{\rho})(\omega)} \frac{\partial Re(\hat{\rho}(\omega))}{\partial m_i}\\
    \frac{\partial -Im(\hat{\rho}(\omega))}{\partial \rho_0} &= \sum_{i=1}^N m_i \frac{(\omega 10^{s_i})}{1 + (\omega 10^{s_i})^2}\\
    \frac{\partial -Im(\hat{\rho}(\omega))}{\partial m_k} &= \rho_0 \cdot \frac{(\omega 10^{s_k})}{1 + (\omega 10^{s_k})^2}

We expect the imaginary part of the resistivity to be negative for most use
cases. For simplified handling, we use :math:`-Im(\hat{\rho})`. In addition, the real part usually is one or two orders of magnitude larger than the imaginary part. Because it is always positive, we can apply the transformation :math:`Re(\rho) \rightarrow log_{10}(Re(\rho))`.

The forward model will be formulated using a real valued function by stacking real and imaginary part on top:

.. math::

  \underline{f}^{linear}(\underline{m}) = \begin{pmatrix}Re(\hat{\rho}(\omega_1))\\ \vdots \\ Re(\hat{\rho}(\omega_K))\\ -Im(\hat{\rho}(\omega_1))\\ \vdots \\  -Im(\hat{\rho}(\omega_k))\end{pmatrix} \quad \quad \underline{f}^{log}(\underline{m}) = \underline{f}(\underline{m}) = \begin{pmatrix}log_{10}(Re(\hat{\rho}(\omega_1)))\\ \vdots \\ log_{10}(Re(\hat{\rho}(\omega_K)))\\ -Im(\hat{\rho}(\omega_1))\\ \vdots \\ -Im(\hat{\rho}(\omega_k))\end{pmatrix} \quad \quad \text{with } \underline{m} = \begin{pmatrix} \rho_0\\ g_1\\ \vdots \\ g_P \end{pmatrix}


Formulation in rho0 and log10(mi)
---------------------------------

Substitute:

* :math:`g_i = log_{10}(m_i)`

.. math::

    \Rightarrow Re(\hat{\rho}(\omega)) &= \rho_0 -  \rho_0 \sum_{i=1}^N 10^{g_i} \frac{(\omega 10^{s_i})^2}{1 + (\omega 10^{s_i})^2}\\
    \Rightarrow -Im(\hat{\rho}(\omega)) &= \rho_0 \sum_{i=1}^N 10^{g_i} \frac{(\omega 10^{s_i})}{1 + (\omega 10^{s_i})^2}\\
    \frac{\partial Re(\hat{\rho}(\omega))}{\partial \rho_0} &= 1 - \sum_{i=1}^N 10^{g_i} \frac{(\omega 10^{s_i})^2}{1 + (\omega 10^{s_i})^2}\\
    \frac{\partial Re(\hat{\rho}(\omega))}{\partial g_k} &= -\rho_0 \cdot log_e{10} \cdot  10^{g_k} \frac{(\omega 10^{s_k})^2}{1 + (\omega 10^{s_k})^2}\\
    \frac{\partial log_{10}(Re(\hat{\rho})(\omega))}{\partial \rho_0} &= \frac{1}{log_e{10}} \frac{\partial log_e(Re(\hat{\rho}))(\omega)}{\partial  \rho_0} = \frac{1}{log_e{10}} \frac{1}{Re(\hat{\rho})(\omega)} \frac{\partial Re(\hat{\rho}(\omega))}{\partial \rho_0}\\
    \frac{\partial log_{10}(Re(\hat{\rho})(\omega))}{\partial g_i} &= \frac{1}{log_e{10}} \frac{\partial log_e(Re(\hat{\rho}))(\omega)}{\partial  g_i} = \frac{1}{log_e{10}} \frac{1}{Re(\hat{\rho})(\omega)} \frac{\partial Re(\hat{\rho}(\omega))}{\partial g_i}\\
    \frac{\partial -Im(\hat{\rho}(\omega))}{\partial \rho_0} &= \sum_{i=1}^N 10^{g_i} \frac{(\omega 10^{s_i})}{1 + (\omega 10^{s_i})^2}\\
    \frac{\partial -Im(\hat{\rho}(\omega))}{\partial g_k} &= \rho_0 \cdot log_e{10} \cdot 10^{g_k} \frac{(\omega 10^{s_k})}{1 + (\omega 10^{s_k})^2}

Formulation in log10(rho0) and log10(mi)
----------------------------------------

Remember:

* :math:`\frac{\partial}{\partial x} \cdot 10^x = log_e(10) 10^x`
* :math:`log_{10}(F(x)) = \frac{log_e(F(x))}{log_e(10)}`
* :math:`\frac{\partial}{\partial x} log_{10}(F(x)) = \frac{1}{log_e(10)} \cdot \frac{1}{F(x)} \cdot \frac{\partial F(x)}{\partial x}`

Substitute:

* :math:`g_i = log_{10}(m_i)`
* :math:`f_0 = log_{10}(\rho_0)`

.. math::

    \Rightarrow Re(\hat{\rho}(\omega)) &= 10^{f_0} - 10^{f_0} \sum_{i=1}^N 10^{g_i} \frac{(\omega 10^{s_i})^2}{1 + (\omega 10^{s_i})^2}\\
    \Rightarrow -Im(\hat{\rho}(\omega)) &= \sum_{i=1}^N 10^{f_0} 10^{g_i} \frac{(\omega 10^{s_i})}{1 + (\omega 10^{s_i})^2}\\
    \frac{\partial Re(\hat{\rho}(\omega))}{\partial f_0} &= log_e(10) 10^{f_0} - log_e(10) 10^{f_0} \sum_{i=1}^N 10^{g_i} \frac{(\omega 10^{s_i})^2}{1 + (\omega 10^{s_i})^2}\\
    \frac{\partial Re(\hat{\rho}(\omega))}{\partial g_k} &= -10^{f_0} \cdot log_e{10} \cdot  10^{g_k} \frac{(\omega 10^{s_k})^2}{1 + (\omega 10^{s_k})^2}\\
    \frac{\partial log_{10}(Re(\hat{\rho})(\omega))}{\partial f_0} &= \frac{1}{log_e(10)} \cdot \frac{1}{Re(\hat{\rho}(\omega))} \cdot \frac{\partial Re(\hat{\rho}(\omega))}{\partial f_0}\\
    \frac{\partial log_{10}(Re(\hat{\rho})(\omega))}{\partial g_k} &= \frac{1}{log_e(10)} \cdot \frac{1}{Re(\hat{\rho}(\omega))} \cdot \frac{\partial Re(\hat{\rho}(\omega))}{\partial g_k}\\
    \frac{\partial -Im(\hat{\rho}(\omega))}{\partial f_0} &= log_e(10) \cdot \sum_{i=1}^N 10^{f_0} 10^{g_i} \frac{(\omega 10^{s_i})}{1 + (\omega 10^{s_i})^2} \\
    \frac{\partial -Im(\hat{\rho}(\omega))}{\partial g_k} &= 10^{f_0} \cdot log_e{10} \cdot 10^{g_k} \frac{(\omega 10^{s_k})}{1 + (\omega 10^{s_k})^2}

Jacobian
--------

The Jacobian of :math:`\underline{f}(\underline{m})` is defined as:

.. math::

  \underline{\underline{J}}_{ij} = \begin{pmatrix}\underline{\frac{\partial
  Re(\hat{\rho}(\omega_i))}{\partial p_j}}\\\underline{\frac{\partial
  -Im(\hat{\rho}(\omega_i))}{\partial p_j}}\end{pmatrix}

As such it is a (2 F x M) matrix, with F the number of frequencies and M the
number of patameters.

.. math::

  \underline{\underline{J}}^{Re}_{linear} &= \begin{bmatrix} \frac{\partial
  Re(\hat{\rho}(\omega_1))}{\partial \rho_0} & \frac{\partial
  Re(\hat{\rho}(\omega_1))}{\partial g_1} & \cdots & \frac{\partial
  Re(\hat{\rho}(\omega_1))}{\partial g_P}\\ \vdots & \ddots & & \vdots\\
  \frac{\partial Re(\hat{\rho}(\omega_m))}{\partial \rho_0} & \frac{\partial
  Re(\hat{\rho}(\omega_m))}{\partial g_1} & \cdots & \frac{\partial
  Re(\hat{\rho}(\omega_m))}{\partial g_P} \end{bmatrix}\\
  \underline{\underline{J}}^{-Im}_{linear} &= \begin{bmatrix} \frac{\partial
  -Im(\hat{\rho}(\omega_1))}{\partial \rho_0} & \frac{\partial
  -Im(\hat{\rho}(\omega_1))}{\partial g_1} & \cdots & \frac{\partial
  -Im(\hat{\rho}(\omega_1))}{\partial g_P}\\ \vdots & \ddots & & \vdots\\
  \frac{\partial -Im(\hat{\rho}(\omega_m))}{\partial \rho_0} & \frac{\partial
  -Im(\hat{\rho}(\omega_m))}{\partial g_1} & \cdots & \frac{\partial
  -Im(\hat{\rho}(\omega_m))}{\partial g_P} \end{bmatrix}\\
  \Rightarrow \underline{\underline{J}}^{linear} &=
  \begin{bmatrix}\underline{\underline{J}}^{Re}_{linear}\\\underline{\underline{J}}^{-Im}_{linear}\end{bmatrix}

The Jacobian of :math:`\underline{f}^{log}` can now be computed using the chain
rule:

.. math::

  \frac{\partial log_{10}(Z(Y))}{\partial Y} &= \frac{\partial
  log_{10}(Z)}{\partial Z} \cdot \frac{\partial Z}{\partial Y} = \frac{1}{Z
  \cdot log_e{10}} \cdot \frac{\partial Z}{\partial Y}\\
  \Rightarrow \underline{\underline{J}} &= \begin{bmatrix} \frac{\partial
  log_{10}(Re)(\hat{\rho}(\omega_1))}{\partial \rho_0} & \frac{\partial
  log_{10}(Re)(\hat{\rho}(\omega_1))}{\partial g_1} & \cdots & \frac{\partial
  log_{10}(Re)(\hat{\rho}(\omega_1))}{\partial g_P}\\ \vdots & \ddots & &
  \vdots\\ \frac{\partial log_{10}(Re)(\hat{\rho}(\omega_m))}{\partial \rho_0}
  & \frac{\partial log_{10}(Re)(\hat{\rho}(\omega_m))}{\partial g_1} & \cdots &
  \frac{\partial log_{10}(Re)(\hat{\rho}(\omega_m))}{\partial g_P} \\
  \frac{\partial -Im(\hat{\rho}(\omega_1))}{\partial \rho_0} & \frac{\partial
  -Im(\hat{\rho}(\omega_1))}{\partial g_1} & \cdots & \frac{\partial
  -Im(\hat{\rho}(\omega_1))}{\partial g_P}\\ \vdots & \ddots & & \vdots\\
  \frac{\partial -Im(\hat{\rho}(\omega_m))}{\partial \rho_0} & \frac{\partial
  -Im(\hat{\rho}(\omega_m))}{\partial g_1} & \cdots & \frac{\partial
  -Im(\hat{\rho}(\omega_m))}{\partial g_P} \end{bmatrix}\\
  &= \begin{bmatrix} \frac{1}{Re(\hat{\rho}(\omega_1)) log_e(10)} \cdot
  \frac{\partial Re(\hat{\rho})(\omega_1)}{\partial \rho_0} &
  \frac{1}{Re(\hat{\rho}(\omega_1)) log_e(10)} \cdot \frac{\partial
  Re(\hat{\rho}(\omega_1))}{\partial g_1} & \cdots &
  \frac{1}{Re(\hat{\rho}(\omega_1)) log_e(10)} \cdot\frac{\partial
  Re(\hat{\rho}(\omega_1))}{\partial g_P}\\ \vdots & \ddots & & \vdots\\
  \frac{1}{Re(\hat{\rho}(\omega_K)) log_e(10)} \cdot \frac{\partial
  Re(\hat{\rho})(\omega_K)}{\partial \rho_0} &
  \frac{1}{Re(\hat{\rho}(\omega_K)) log_e(10)} \cdot \frac{\partial
  Re(\hat{\rho}(\omega_K))}{\partial g_1} & \cdots &
  \frac{1}{Re(\hat{\rho}(\omega_K)) log_e(10)} \cdot\frac{\partial
  Re(\hat{\rho}(\omega_K))}{\partial g_P}\\ \frac{\partial
  -Im(\hat{\rho})(\omega_1)}{\partial \rho_0} &  \frac{\partial
  -Im(\hat{\rho}(\omega_1))}{\partial g_1} & \cdots &  \frac{\partial
  -Im(\hat{\rho}(\omega_1))}{\partial g_P}\\ \vdots & \ddots & & \vdots\\
  \frac{\partial -Im(\hat{\rho})(\omega_K)}{\partial \rho_0} & \frac{\partial
  -Im(\hat{\rho}(\omega_K))}{\partial g_1} & \cdots & \frac{\partial
  -Im(\hat{\rho}(\omega_K))}{\partial g_P}\end{bmatrix}\\
