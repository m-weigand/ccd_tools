
Introduction
============

This project is a collection of Python libraries and scripts which facilitate
the analysis of spectral induced polarisation (SIP) spectra using a Debye
decomposition scheme (see :doc:`dd_general` for general notes on the Debye
decomposition scheme). The basis of all programs is formed by the *GeccoInv*
library which implements a somewhat general multi-dimensional inversion scheme
which supports an arbitrary number of regularizations between various
dimensions. Building upon these, three front-ends for the Debye Decompositions
are provided:

* :doc:`programs/dd_single` fits an arbitrary number of SIP spectra without any
  kind of regularization between the spectra.
* :doc:`programs/dd_time` fits an arbitrary number of time-lapse SIP spectra with a
  regularization on the time axis (separate regularization parameters for
  :math:`\rho_0` and the chargeabilities :math:`m_i`)
* :doc:`programs/dd_space_time` fits and arbitrary number of time-lapse SIP spectra
  recovered from imaging results with the same time regularization as applied
  by *dd_time.py*. No spatial regularization is applied.

See :doc:`fit_routines` for detailed information on each of the front-ends.

Each front-end is accompanied by a post processing tool (*ddps.py*, *ddpt.py*,
and *ddpst.py*) which allows various analysis and postprocessing steps to be
applied on inversion results. This includes filtering and plotting routines.
(TODO: Link).

Feedback, bug reports, and general advice is always welcome. Please use the
issue tracker on the github page for communication
(https://github.com/m-weigand/dd_interfaces).  Before you report a bug make sure to
look through the existing bugs; perhaps your problem was already reported. Also
make sure to include all necessary information to reproduce the bug. A small
example data set and the command line options to trigger the bug are always
helpfull!


Copyright
---------

DD_Interfaces is licenced under the GPL 3 or later
(https://www.gnu.org/licenses/licenses.html#GPL).
