
Introduction
============

The Debye decomposition tools provide a set of Python programs to fit
electrical complex resistivity spectra (or Spectral Induces Polarisation, SIP,
spectra) using a Debye decomposition scheme (see section :doc:`theory` for an
theoretical overview of the implemented methods). In addition to the
independent decomposition of one or more spectra, a smoothing regularisation
can be applied between multiple spectra, i.e. if the spectra belong to a
time-lapse measurement, and only smooth changes are expected.

The installation for Windows and Linux is described in the section
:doc:`installation`, and the section :doc:`getting_started` provides first
usage instructions.

Please note that the name of the project suggests that only the Debye
decomposition is implemented here. However, work has progress relatively far in
implementing the more general case of a Cole-Cole decomposition, in which the
parameter *c* can be freely chosen between 0 and 1.

If you are looking for a classic Cole-Cole fit using only one term, have a look
at https://github.com/m-weigand/Cole-Cole-fit.

Two primary decomposition programs are provided:

* :doc:`programs/dd_single` fits an arbitrary number of SIP spectra without any
  kind of regularization between the spectra.
* :doc:`programs/dd_time` fits an arbitrary number of time-lapse SIP spectra with a
  regularization on the time axis (separate regularization parameters for
  :math:`\rho_0` and the chargeabilities :math:`m_i`)

See :doc:`fit_routines` for a complete list of the provided programs, and
detailed description of the input parameters.

Each front-end is accompanied by a post processing tool (*ddps.py*, *ddpt.py*)
which allows various analysis and postprocessing steps to be applied on
inversion results. This includes filtering and plotting routines.

Within this documentation, the term "Debye decomposition tools" referes to the
ready-to-use distribution of the decomposition tools. This distribution is
composed of two python subprojects: *geccoinv* and *dd_interfaces*. *geccoinv*
contains the multi-dimensional inversion framework used for the decomposition
process, while *dd_interfaces* includes the forward formulation of the
Decomposition process, and the frontends used to apply the implemented methods.
For end-users, it is always recommended to use the "debye decomposition tools",
if in doubt.

Feedback, bug reports, and general advice is always welcome. Please use the
issue tracker on the github pages for communication
(https://github.com/m-weigand/Debye_Decomposition_Tools).  Before you report a
bug, make sure to search the existing bugs (issues) for a relevant item.  Also
make sure to include all necessary information to reproduce the bug. A small
example, including data set and batch file to trigger the bug, are always
helpful!

Separate repositories are maintained for *geccoing* and *dd_interfaces* (only
relevant if you plan on changing the code):

* https://github.com/m-weigand/geccoinv
* https://github.com/m-weigand/dd_interfaces

The Debye decomposition tools (including the components "DD_Interfaces" and
"geccoinv") are  licenced under the GPL 3 or later
(https://www.gnu.org/licenses/licenses.html#GPL).

.. note::

    If you are reading this manual as a PDF file, please note that download
    links do not work. Please refer to the corresponding HTML version for these
    links.
