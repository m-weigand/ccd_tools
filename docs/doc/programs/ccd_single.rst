ccd_single
----------

*ccd_single* is used to fit one or multiple SIP spectra using the Debye (or
Cole-Cole) decomposition scheme. No smoothing regularization between the
spectra is applied.

.. toctree::

   ../environment_vars

Command line options
^^^^^^^^^^^^^^^^^^^^

.. program-output:: ccd_single -h

Usage Examples
^^^^^^^^^^^^^^

.. note::

    Beware of the chargeability distribution at the frequency edges: Here the
    distribution is often dominated by the starting model due to low
    sensitivities. However it is advisable to add one frequency decade in
    :math:`\tau` values to the edges.

.. _ref_dd_single_best_pract:

