
Best practices
==============

The following procedure is recommended for new data sets and focuses on
inversions using *dd_single.py* and *dd_time.py*:

* Initially invert with variable :math:`\lambda` values for the frequency
  regularization
* Fine-tune with a fixed lambda (this in general yields more robust results and
  makes results comparable)
* Usually the third starting model yields the most robust results: ::

    DD_STARTING_MODEL=3 dd_single.py ...

* Normalisation can help... : ::

    dd_single.py --norm 10

* For time regularization: here only a fixed lambda can be used. Start with a
  small value and take a look at the maximum regularization strength for the
  time-regularization. The regularization strength is automatically plotted
  when the ``--plot`` option is enabled.

* while the structure of the input files is fixed, the data format can be
  changed using the ``--data_format`` option. Thus a conversion from
  conductivities to resistivities and vice versa is not necessary, as well as a
  conversion between real/imaginary part and magnitude/phase format.

* the ``--tmp`` option can improve execution speed on conventional hard
  drives (for SSDs there shouldn't be any improvement)

