Output Files
^^^^^^^^^^^^

The following sections describe the output files of the various formats.
Formats can be changed using the **--output_format** switch.

ascii_audit format
""""""""""""""""""

This output format saves fit results to ASCII text files. Each text file
contains a header which uniquely identifies the fit run that the results were
created from. In addition, this format tries to group results into one file,
where possible. Using the header information, clear process logs can be
created, and mix-ups of results can be prevented.

This is the default output format.

.. note::

    Can be enabled using the **--output_format ascii_audit** switch

.. note::

    While this output format is great for ensuring a clear processing trail, it
    is currently not possible to directly use the OUTPUT files as INPUT files
    for new decompositions!

header
++++++

Each output file consists of two parts: the header (four lines), and the data
part (the rest of the file). The header looks like this ::

    # id:30ffcd8e-2b75-48f9-acc4-3f93c9c0d48e
    # 20150730_14h:32m
    # /home/mweigand/.local/bin/dd_time.py -f data/frequencies.dat --times data/times.dat\
        -d data/data.dat -o results_time --f_lambda 50\
        --tmi_first_order --tm_i_lambda 5000 --plot
    # covf

* the '#' character indicates a non-data line
* the first line contains a unique id, which is generated for each run of
  either **dd_single.py** or **dd_time.py**. This id changes also for repeated
  runs of the same settings!
* The second line contains a datetime string: first the date in the order
  year-month-day, followed by the hour (24 hours) and minute.
* The third line contains the command call. Note that in the example above, the
  command is stretched over three lines. This is only for display purposes, and
  in the files will always be in one line.
* The fourth line contains the data header, indicating the type of data
  (sometimes even column descriptions).
  results/

Files
+++++

A typical result directory in this format contains the following files ::

    |-- covf.dat
    |-- covm.dat
    |-- data.dat
    |-- errors.dat
    |-- f.dat
    |-- frequencies.dat
    |-- integrated_paramaters.dat
    |-- inversion_options.json
    |-- lams_and_nr_its.dat
    |-- m_i.dat
    |-- normalization_factors.dat
    |-- tau.dat
    |-- times.dat
    `-- version.dat

    0 directories, 14 files

.. include:: output_files/covf.dat.txt

.. include:: output_files/covm.dat.txt

.. include:: output_files/data.dat.txt

.. include:: output_files/errors.dat.txt

.. include:: output_files/f.dat.txt

* *frequencies.dat*: Frequencies [Hz], each line contains one frequency, in
  ascending order.

* *integrated_paramaters.dat*: Contains the integrated parameters as computed
  from the RTD. Each line contains the parameters of one spectrum, with the
  columns decribed in the header.

* inversion_options.json*: inversion options (as set by command line options,
  primarily for debug purposes)

* *lams_and_nr_its.dat*:

* *m_i.dat*: RTDs for all spectra. Each line contains the RTD of one spectrum.

* *normalization_factors.dat*: Normalisation factors used (will only be created
  if the `--norm` option was activated.

.. include:: output_files/tau.dat.txt

* *times.dat*: times corresponding to the spectra (only created by *dd_time.py*

.. include:: output_files/version.dat.txt


ascii format
""""""""""""

This output format saves the files to ASCII text files. Most
parameters/variables are saved to a separate file, resulting in a large number
of files. No, or only very limited, headers are provided. This format can make
postprocessing easy, but should only be used if really necessary.

.. note::

    can be enabled using the **--output_format ascii** switch

A typical result directory in this format contains the following files ::

    results/
    |-- command.dat
    |-- data.dat
    |-- data_format.dat
    |-- errors.dat
    |-- f.dat
    |-- f_format.dat
    |-- frequencies.dat
    |-- inversion_options.json
    |-- lambdas.dat
    |-- normalization_factors.dat
    |-- nr_iterations.dat
    |-- omega.dat
    |-- rms_definition.json
    |-- s.dat
    |-- stats_and_rms
    |   |-- covf_results.dat
    |   |-- covm_results.dat
    |   |-- decade_bins_results.dat
    |   |-- decade_loadings_results.dat
    |   |-- f_50_results.dat
    |   |-- f_arithmetic_results.dat
    |   |-- f_geometric_results.dat
    |   |-- f_max_results.dat
    |   |-- f_mean_results.dat
    |   |-- f_peak1_results.dat
    |   |-- f_peak2_results.dat
    |   |-- f_peaks_all_results.dat
    |   |-- m_data_results.dat
    |   |-- m_i_results.dat
    |   |-- m_tot_n_results.dat
    |   |-- m_tot_results.dat
    |   |-- rho0_results.dat
    |   |-- rms_all_error.dat
    |   |-- rms_all_noerr.dat
    |   |-- rms_imag_parts_error.dat
    |   |-- rms_imag_parts_noerr.dat
    |   |-- rms_real_parts_error.dat
    |   |-- rms_real_parts_noerr.dat
    |   |-- tau_50_results.dat
    |   |-- tau_arithmetic_results.dat
    |   |-- tau_geometric_results.dat
    |   |-- tau_max_results.dat
    |   |-- tau_mean_results.dat
    |   |-- tau_peak1_results.dat
    |   |-- tau_peak2_results.dat
    |   |-- tau_peaks_all_results.dat
    |   `-- U_tau_results.dat
    |-- tau.dat
    `-- version.dat

    1 directory, 48 files

The following output files will be created in the selected output directory.
These files are described below, sorted by category.

Input data
++++++++++

.. include:: output_files/data.dat.txt

* *data_format.dat* contains the data format in the format usable with the
  ``--data_format`` command line option (usually **cre_cim**).
* Frequencies and corresponding angular frequencies (
   :math:`\omega = 2 \cdot \pi \cdot f`) are stored in the files
   *frequencies.dat* and *omega.dat*.
* The file *command.dat* holds the complete call to the fit routine
* A JSON formatted file *inversion_options.json* stores internal inversion
  options. This file is mainly for debugging purposes, and needed to recreated
  inversion objects from fit results.
* *rho_normalizations.dat* contains normalization factors if the option
  ``--norm_mag`` was used.

*dd_time.py* only:

* the file *times.dat* contains the time strings as read from the input files.
  One time per line.

Filter results
++++++++++++++

.. note::

    Filtering using `ddps.py` is still an experimental feature and might not
    work at the moment.

* *filter_mask.dat* contains the remaining indices after a filter operation
  with `ddps.py`

Primary fit results
+++++++++++++++++++

* :math:`\tau` and :math:`s = log_{10}(\tau)` values are stored in the files
  *tau.dat* and *s.dat*, respectively.

* The regularization parameters of the last iterations are stored in the file
  *lambdas.dat*, one per line:

  ::

    1.000000000000000021e-03
    1.000000000000000056e-01

* The chargeability values of the last iteration can be found in
  *stats_and_rms/m_i_results.dat*

.. include:: output_files/f.dat.txt

* RMS values are stored in the subdirectory *stats_and_rms*, using the
  following files (final RMS of each spectrum per line). *real/imag* here
  correspond to real part and imaginary part of resistivity, respectively. The
  *_error* suffix denotes RMS values computed with data weighting.

  ==========================  ==========================================================
  filename                    description
  ==========================  ==========================================================
  *rms_all_error.dat*         RMS of real and imaginary parts, including error weighting
  *rms_all_noerr.dat*         RMS of real and imaginary parts, without error weighting
  *rms_imag_parts_error.dat*  Error weighted RMS of imaginary parts
  *rms_imag_parts_noerr.dat*  Non-error weighted RMS of imaginary parts
  *rms_real_parts_error.dat*  Error weighted RMS of real parts
  *rms_real_parts_noerr.dat*  Non-error weighted RMS of real parts
  ==========================  ==========================================================

    .. math::

        RMS_{\text{no error}} = \sqrt{\frac{1}{N} \sum_i^N d_i - f_i(m)}\\
        RMS_{\text{with error}} = \sqrt{\frac{1}{N} \sum_i^N \frac{d_i - f_i(m)}{\epsilon_i}}

* The number of iterations actually used for each spectrum are stored in *nr_iterations.dat*.

.. include:: output_files/errors.dat.txt

* Normalization factors are stored in *normalization_factors.dat*

.. include:: output_files/version.dat.txt

Integral parameters
+++++++++++++++++++

Statistical parameters are stored in the subdirectory *stats_and_rms*, and all
output files have the same file format. Each line contains the value of one
spectrum. This applies to the following files (N = number of frequencies, M =
number of parameters):

=============================  ===============================
filename                       stored values per line
=============================  ===============================
*m_i_results.dat*              :math:`m(\tau_i)`
*m_tot_n_results.dat*          :math:`log_{10}(m_{tot}^n)`
*m_tot_results.dat*            :math:`log_{10}(m_{tot}^n)`
*rho0_results.dat*             :math:`log_{10}(\rho_0)`
*tau_50_results.dat*           :math:`log_{10}(\tau_{50})`
*tau_mean_results.dat*         :math:`log_{10}(\tau_{mean})`
*tau_arithmetic_results.dat*   :math:`log_{10}(\tau_{arithmetic})`
*tau_geometric_results.dat*    :math:`log_{10}(\tau_{geometric})`
*tau_peak1_results.dat*        :math:`log_{10}(\tau_{peak}^1)`
*tau_peak2_results.dat*        :math:`log_{10}(\tau_{peak}^2)`
*tau_peaks_all_results.dat*    :math:`log_{10}(\tau_{peak}^i)`
*tau_x_\*.dat*                 :math:`log_{10}(\tau_x)`; see description below
*tau_max.dat*                  :math:`\tau` corresponding to max. chargeability. First occurence.
*U_tau_results.dat*            Uniformity parameter :math:`U_{\tau} = \frac{\tau_{60}}{\tau_{10}}`
*f_50_results.dat*             frequency corresponding to :math:`\tau_{50}`
*f_mean_results.dat*           frequency corresponding to :math:`\tau_{mean}`
*f_peak1_results.dat*          frequency corresponding to :math:`\tau_{peak}^1`
*f_peak2_results.dat*          frequency corresponding to :math:`\tau_{peak}^2`
*f_peaks_all_results.dat*      frequency corresponding to all peaks :math:`\tau_{peak}^N`
*covf_results.dat*             coverage frequencies (N columns)
*covm_results.dat*             coverage parameters (M columns)
=============================  ===============================

Integral parameters are explained in the section :ref:`int_pars`.

