dd_time.py
==========


Command line options
--------------------

.. program-output:: dd_time.py -h

Usage Examples
--------------

Output Format
-------------

The output file match the output files of the :doc:`dd_single`
program (see here for detailed documentation of all output files:
:ref:`ref_dd_single_output_format`) except for the following changes:

* the file *times.dat* contains the time strings as read from the input files.
  One time per line.

* *rho_normalizations.dat* contains normalization factors if the option
  ``--norm_mag`` was used.
