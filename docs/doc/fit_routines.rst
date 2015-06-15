
.. toctree::
    :maxdepth: 1
    :hidden:

    programs/dd_single
    programs/dd_time
    programs/dd_space_time


Fit Routines
============

Three fit routines are provided with specialised input/output configurations:

* Fiting of separate sepctra (1D) :doc:`programs/dd_single`
* Fitting of time-regularized spectra (2D) :doc:`programs/dd_time`
* Fitting of spatially distributed time-regularized spectra (3D, but no spatial
  regularization) :doc:`programs/dd_space_time`

Each fit routine can use one of the following kernels (i.e. models) to descripe
the SIP spectra:

* Resistivity Debye decomposition
* Conductivity Debye decomposition

Non-linear fits are highly dependent on the starting models to use. Read more
about the available starting models here:

:doc:`starting_models`

