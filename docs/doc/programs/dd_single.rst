dd_single.py
------------

This program is used to fit one or multiple
SIP-spectra in one go. There is no regularization between the spectra.

For detailed information on command line options and usage please refer to the
sections below. Also note the :ref:`ref_dd_single_best_pract` section.

Command line options
^^^^^^^^^^^^^^^^^^^^

.. program-output:: dd_single.py -h

Usage Examples
^^^^^^^^^^^^^^

.. note::

    Beware of the chargeability distribution at the frequency edges: Here the
    distribution is often dominated by the starting model due to low
    sensitivities. However it is advisable to add one frequency decade in
    :math:`\tau` values to the edges.

.. _ref_dd_single_best_pract:

Usage example 1
"""""""""""""""

You need a frequency file which contains the frequencies, each in a seperate
line, in ascending order:

frequency.dat: ::

    0.463
    1.000
    2.128
    4.545
    10.000
    14.706
    21.277
    27.778
    29.412
    50.000
    58.824
    70.000

Complex resistivity spectra are provided using a data file which holds a
spectrum in each line. Columns are separated by space and values are linear
both for magnitude and phase values. The first N columns correspond to the
magnitude values (:math:`\Omega m`) corresponding to the frequencies stored in
*frequencies.dat*. The following N columns represent the corresponding phase
values.

data.dat: ::

    17.9984 17.9897 17.9792 17.9636 18.0217 18.0235 18.0817 18.0135 18.0854 18.0856 18.0816 18.0802 18.0777 18.0770 18.0747 18.0748 18.0748 18.0738 18.0757 18.0790 -1.2674 -2.1537 -2.7997 -3.7206 -3.1617 -3.8350 -0.2499 -3.8007 -3.7300 -2.9362 -3.4580 -3.3821 -3.1575 -3.0282 -3.0008 -2.7883 -2.7889 -2.6931 -2.3717 -1.9792
    17.9983 17.9896 17.9790 17.9633 18.0217 18.0235 18.0817 18.0135 18.0854 18.0856 18.0816 18.0802 18.0777 18.0769 18.0747 18.0748 18.0747 18.0738 18.0757 18.0790 -1.2790 -2.1838 -2.8497 -3.7900 -3.2634 -3.9336 -0.2695 -3.8899 -3.8167 -2.9599 -3.5263 -3.4432 -3.2061 -3.0744 -3.0456 -2.8269 -2.8222 -2.7246 -2.3927 -1.9903

The spectra can now be fitted to a Debye decomposition using the command:

::

    dd_single.py -f frequencies.dat -d data.dat -o dd_results/

Results will be written to the subdirectory **dd_results/**

.. _ref_dd_single_output_format:


