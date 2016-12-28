Profiling and Debugging
=======================

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

Debugging notes
---------------

Random collection of notes:

* We have to save all inputs from the dicts in order to recreate an inversion
  (we need to reconstruct the whole inversion object for that). Therefore we
  should simplify the various dicts involved.

* For each iteration we want:

 * Sensitivities
 * Resolution matrix (covariance matrix)
 * Cumulative sensitivities
 * Data covariance matrix
 * Model covariance matrix

.. toctree::

    dd_testing_res_inv

