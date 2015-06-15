.. DD_Interfaces documentation master file, created by
   sphinx-quickstart on Mon Jun 17 09:29:21 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=============
DD_Interfaces
=============


.. toctree::
    :maxdepth: 1

    introduction
    installation
    fit_routines
    starting_models



Debye Decomposition
===================

.. toctree::

    dd_general

DD in conductivities
====================

.. toctree::
    dd_conductivity

:doc:`dd_conductivity`

.. toctree::

    dd_theory_eps
    dd_sensitivities
    dd_testing_res_inv

Long-term Todo
==============

The following items are somewhat long-term todo items which could also be seen
as a kind of general development directives.

Organisational things
---------------------

* Explore "interactive" fitting using IPython
* Clean up interface
* Clean up test cases

Functionality
-------------

* We need to check for numdifftools in order to run the unit tests!
* Reach full test coverage
* logfile should be in order (even for multiprocessing, perhaps merge logfiles later?)

Long-term:

* Implement c not equal 1 routines
* GSVD solution for Tikhonov first order reg.
* Determine lambda from the l-curve
* Implement univariate lambda search
* SVD - analysis

Profiling and Debugging
-----------------------

Things go wrong. If something goes wrong with memory usage, use the
`memory_profiler` module (https://github.com/fabianp/memory_profiler):

::

    pip install memory_profiler


At least in *dd_singly.py* there is a commented import line: ::

    import memory_profiler
    
Just add the decorator `@profile` in front of any function to get a
line-by-line memory usage profile printed to STDOUT.

To profile the memory increase between subsequent spectra in **dd_single.py**,
add the decorator to the `fit_one_spectrum` function:

::

    @profile
    def fit_one_spectrum(opts):

Then run the `dd_single.py` command as usual, but redirect the output to a
logfile:

::

    dd_single.py [OPTIONS] | tee logfile

Then grep for specific calls:

::

    grep "run_inversion" logfile
    206     51.9 MiB      3.5 MiB       ND.run_inversion()
    206     54.9 MiB      2.9 MiB       ND.run_inversion()
    206     55.0 MiB      0.1 MiB       ND.run_inversion()
    206     55.1 MiB      0.1 MiB       ND.run_inversion()
    206     55.1 MiB      0.1 MiB       ND.run_inversion()
    206     55.2 MiB      0.1 MiB       ND.run_inversion()
    206     55.2 MiB      0.1 MiB       ND.run_inversion()
    206     55.3 MiB      0.0 MiB       ND.run_inversion()
    206     55.4 MiB      0.1 MiB       ND.run_inversion()
    206     55.4 MiB      0.1 MiB       ND.run_inversion()

As a side note, it would be nice to get `pycallgraph` to run:

http://pycallgraph.slowchop.com/en/master/guide/command_line_usage.html

Sidenote: We could also use Travis (https://travis-ci.org/) von continous
integration.

Notes
-----

* General goal: Resistivity and conductivity formulation, transformation from
  continuous to discrete formulation, inclusion of c (Cole-Cole case)

* The explicit computation of the matrix product
  :math:`\underline{\underline{J}}^T \cdot \underline{\underline{J}}` is
  computationally expensive. When the CG solver is used most of the time this
  product can be prevented by performing the matrix-vector product from right
  to left.


API
===

.. toctree::
    :maxdepth: 0

    api/lib_dd

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
