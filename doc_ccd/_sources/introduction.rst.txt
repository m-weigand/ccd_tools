
Introduction
============

The Cole-Cole decomposition tools provide a set of Python programs to fit
electrical complex resistivity spectra (or Spectral Induced Polarisation, SIP,
spectra/signatures) using a Cole-Cole decomposition scheme (see section
:doc:`theory` for an theoretical overview of the implemented methods). This
also includes the popular Debye decomposition scheme. In addition to the
independent decomposition of one or more spectra, a smoothing regularization
can be applied between multiple spectra for cases of time-lapse data where only
smooth changes between subsequent measurements in a time series are expected.

The installation for Windows and Linux is described in the section
:doc:`installation`, and the section :doc:`getting_started` provides first
usage instructions.

Please note that the Cole-Cole decomposition is, at the moment, only
implemented for the resistivity case. For the conductivity formulation, only
the Debye decompositon (*c = 1*) is implemented.

If you are looking for a classic Cole-Cole fit using only one or two terms,
have a look at https://github.com/m-weigand/Cole-Cole-fit.

Two primary decomposition programs are provided:

* :doc:`programs/ccd_single` fits an arbitrary number of SIP spectra without any
  kind of regularization between the spectra.
* :doc:`programs/ccd_time` fits an arbitrary number of time-lapse SIP spectra with a
  regularization on the time axis (separate regularization parameters for
  :math:`\rho_0` and the chargeabilities :math:`m_i`)

See :doc:`fit_routines` for a complete list of the provided programs, and
detailed description of the input parameters.

Each front-end is accompanied by a post processing tool (*ddps.py*, *ddpt.py*)
which allows various analysis and postprocessing steps to be applied on
inversion results. This includes filtering and plotting routines.

This package depends on two additional python packages, *sip_models* and
*geccoinv*, developed in separate git repositories. They are, however, integral
components of the Cole-Cole decomposition routines.

Separate repositories are maintained for *sip_models*, *geccoinv* and
*ccd_tools*:

* https://github.com/m-weigand/sip_models
* https://github.com/m-weigand/geccoinv
* https://github.com/m-weigand/ccd_tools

Feedback, bug reports, and general advice is always welcome. Please use the
issue tracker on the github pages for communication
(https://github.com/m-weigand/ccd_tools/).  Before you report a bug, make sure
to search the existing bugs (issues) for relevant items. Also, make sure to
include all necessary information to reproduce reported bugs. A small example,
including data set and batch files to trigger the bug, is always helpful!


The Cole-Cole decomposition tools (including the packages "sip_models" and
"geccoinv") are licenced under the GPL 3 or later
(https://www.gnu.org/licenses/licenses.html#GPL).

.. note::

    If you are reading this manual as a PDF file, please note that download
    links do not work. Please refer to the corresponding HTML version for these
    links.
