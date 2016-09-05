"""

"""
import ccd_single_stateless as decomp_single_sl
import numpy as np
from multiprocessing import Pool
import lib_dd.interface as lDDi


class ccd_single(object):
    """Cole-Cole decomposition object
    """

    def __init__(self, config):
        self.config = config

    def _filter_nan_values(self, frequencies, cr_spectrum):
        """
            Filter nan values along the frequency axis (we always ne part1 and
            part2).

            Return filtered frequencies, cr_spectrum
        """

        # check for NaN values
        nan_indices = np.isnan(cr_spectrum)
        nan_along_freq = np.any(nan_indices, axis=1)
        to_delete = np.where(nan_along_freq)
        frequencies_cropped = np.delete(frequencies, to_delete)
        cr_spectrum_cropped = np.delete(cr_spectrum, to_delete, axis=0)
        return frequencies_cropped, cr_spectrum_cropped

    def _get_fit_datas(self, data):
        """
        Prepare data for fitting. Prepare a set of variables/objects for each
        spectrum. Also filter nan values

        Parameters
        ----------
        data : dict containing the keys 'frequencies', 'cr_data'
        """
        fit_datas = []

        nr_of_spectra = len(data['cr_data'])
        for i in range(0, nr_of_spectra):
            fit_data = {}
            fit_data['outdir'] = data['outdir']
            # change file prefix for each spectrum
            # at the moment we need a copy for this
            frequencies_cropped, cr_data = self._filter_nan_values(
                data['frequencies'], data['cr_data'][i])

            fit_data['prep_opts'] = data['prep_opts']
            fit_data['data'] = cr_data
            fit_data['nr'] = i + 1
            fit_data['nr_of_spectra'] = nr_of_spectra
            fit_data['frequencies'] = frequencies_cropped

            # inversion options are changed for each spectrum, so we have to
            # copy it each time
            inv_opts_i = data['inv_opts'].copy()
            inv_opts_i['frequencies'] = frequencies_cropped
            inv_opts_i['global_prefix'] = 'spec_{0:03}_'.format(i)
            if('norm_factors' in data):
                inv_opts_i['norm_factors'] = data['norm_factors'][i]
            else:
                inv_opts_i['norm_factors'] = None

            fit_data['inv_opts'] = inv_opts_i

            fit_datas.append(fit_data)

        return fit_datas

    def fit_data(self, data):
        """This is the central fit function, which prepares the data, fits each
        spectrum, plots (if requested), and then saves the results.
        """
        fit_datas = self._get_fit_datas(data)

        # fit
        if(data['prep_opts']['nr_cores'] == 1):
            print('single processing')
            # single processing
            results = list(map(decomp_single_sl.fit_one_spectrum, fit_datas))
        else:
            # multi processing
            print('multi processing')
            p = Pool(data['prep_opts']['nr_cores'])
            results = p.map(decomp_single_sl.fit_one_spectrum, fit_datas)

        self.results = results
        self.data = data
        # results now contains one or more ND objects
        # iog.save_fit_results(data, results)

    def get_data_dd_single(self, options, outdir):
        """
        Load frequencies and data and return a data dict

        Parameters
        ----------

        options: cmd options


        Returns
        -------
        data: dict with entries "raw_data", "cr_data", "options", "inv_opts",
              "prep_opts"
        """
        data, options = lDDi.load_frequencies_and_data(options)

        # we need list of spectra
        size_y = int(data['raw_data'].shape[1] / 2)
        cr_data = [x.reshape((size_y, 2), order='F') for x in data['raw_data']]

        data['cr_data'] = cr_data

        # we distinguish two sets of options:
        # prep_opts : all settings we need to prepare the inversion (i.e. set
        #             regularization objects)
        # inv_opts : options that are directly looped through to the NDimInv
        # object
        prep_opts, inv_opts = options.split_options()

        data['outdir'] = outdir
        data['options'] = options
        data['prep_opts'] = prep_opts
        data['inv_opts'] = inv_opts
        return data
