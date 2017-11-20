Input Data files
^^^^^^^^^^^^^^^^

You need a frequency file which contains the frequencies, each in a seperate
line, in ascending order:

frequency.dat (:download:`Download frequencies.dat
(unix)<example1_single/frequencies.dat>`)
(:download:`Download frequencies.dat
(Windows)<example1_single/data_windows/frequencies.dat>`): ::

    0.0010
    0.0018
    0.0032
    0.0056
    0.0100
    0.0178
    0.0316
    0.0562
    0.1000
    0.1778
    0.3162
    0.5623
    1.0000
    1.7783
    3.1623
    5.6234
    10.0000
    17.7828
    31.6228
    56.2341
    100.0000
    177.8279
    316.2278
    562.3413
    1000.0000

Complex resistivity spectra are provided using a data file which holds a
spectrum in each line. Columns are separated by space and values are linear
both for magnitude and phase values. The first N columns correspond to the
magnitude values (:math:`\Omega m`) corresponding to the frequencies stored in
*frequencies.dat*. The following N columns represent the corresponding phase
values.

data.dat
(:download:`download data.dat (unix)<example1_single/data.dat>`)

(:download:`download data.dat (Windows)
<example1_single/data_windows/data.dat>`)

::

    49.345594 49.120225 48.860658 48.589371 48.333505 48.113950 47.939222\
    47.807051 47.709583 47.637735 47.583349 47.539704 47.501267 47.463162\
    47.420588 47.368190 47.299354 47.205358 47.074354 46.890271 46.632118\
    46.274900 45.794402 45.178163 44.441082 -10.526822 -12.095446 -13.004975\
    -12.999086 -12.088092 -10.544173 -8.744458 -7.007706 -5.526119 -4.380307\
    -3.584099 -3.124956 -2.990678 -3.184856 -3.735642 -4.701107 -6.172278\
    -8.272438 -11.148023 -14.941904 -19.734922 -25.441545 -31.665354\
    -37.581057 -41.99903



.. note::

    The previous listing for the data.dat file contains only one line. For
    display purposes, line breaks were introduced, and indicated by '\\'
    characters.

Input data formats
""""""""""""""""""

Input data in `data.dat` can be specified in various formats (internally
converted using the :py:mod:`sip_formats.convert`) module:

* *lnrmag_rpha*: The first N columns are resistivity magnitudes in the natural
  logarithm; the second N columns contain resistivity phase values (mrad)
* *log10rmag_rpha*: The first N columns are resistivity magnitudes in the
  base-10 logarithm; the second N columns contain resistivity phase values
  (mrad)
* *rmag_rpha*: The first N columns are linear resistivity magnitudes; the
  second N columns contain resistivity phase values (mrad)
* *rre_rim*: The first N columns contain resistivity real parts; the second N
  columns contain resistivity imaginary parts
* *rre_rmim*: The first N columns contain resistivity real parts; the second N
  columns contain the negative of resistivity imaginary parts
* *cmag_cpha*: The first N columns contain conductivity magnitudes, the second N
  columns contain conductivity phase values
* *cre_cim*: The first N columns contain conductivity real parts; the second N
  columns contain conductivity imaginary parts
* *cre_cmim*: The first N columns contain conductivity real parts; the second N
  columns contain the negative of conductivity imaginary parts

N is the number of frequencies. Specify the data format using the
:command:`\-\-data_format` command line option. For example, to use
conductivity real and imaginary parts as input data, use::

    ccd_tools --data_format cre_cim ...

Output Files
^^^^^^^^^^^^

The following sections describe the output files of the various formats.
Formats can be changed using the :command:`--output_format` switch.

ascii_audit format
""""""""""""""""""

This output format saves fit results to ASCII text files. Each text file
contains a header which uniquely identifies the fit run that the results were
created from. In addition, this format tries to group results into one file,
where possible. Using the header information, clear process logs can be
created, and mix-ups of results can be prevented.

This is the default output format.

.. note::

    Can be enabled using the :command:`--output_format ascii_audit` switch

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
    # /home/mweigand/.local/bin/cdd_time -f data/frequencies.dat --times data/times.dat\
        -d data/data.dat -o results_time --f_lambda 50\
        --tmi_first_order --tm_i_lambda 5000 --plot
    # covf

* the '#' character indicates a non-data line
* the first line contains a unique id, which is generated for each run of
  either **ccd_single** or **ccd_time**. This id changes also for repeated
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

* *normalization_factors.dat*: Normalization factors used (will only be created
  if the :command:`--norm` option was activated.

.. include:: output_files/tau.dat.txt

* *times.dat*: times corresponding to the spectra (only created by *ccd_time*

.. include:: output_files/version.dat.txt


ascii format
""""""""""""

This output format saves the files to ASCII text files. Most
parameters/variables are saved to a separate file, resulting in a large number
of files. No, or only very limited, headers are provided. This format can make
postprocessing easy, but should only be used if really necessary.

.. note::

    can be enabled using the :command:`--output_format ascii` switch

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
  :command:`--data_format` command line option (usually **cre_cim**).
* Frequencies and corresponding angular frequencies (
   :math:`\omega = 2 \cdot \pi \cdot f`) are stored in the files
   *frequencies.dat* and *omega.dat*.
* The file *command.dat* holds the complete call to the fit routine
* A JSON formatted file *inversion_options.json* stores internal inversion
  options. This file is mainly for debugging purposes, and needed to recreated
  inversion objects from fit results.
* *rho_normalizations.dat* contains normalization factors if the option
  :command:`--norm_mag` was used.

*ccd_time* only:

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
