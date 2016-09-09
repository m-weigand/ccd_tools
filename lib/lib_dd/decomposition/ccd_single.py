"""

"""
import os
import ccd_single_stateless as decomp_single_sl
from multiprocessing import Pool
import lib_dd.interface as lDDi
import lib_dd.config.cfg_single as cfg_single


class ccd_single(object):
    """Cole-Cole decomposition object
    """

    def __init__(self, config=None):
        if config is None:
            config = cfg_single.cfg_single()
        self.config = config

        # this will be filled by self.get_data_dd_single
        self.data = None

    def fit_data(self):
        """This is the central fit function, which prepares the data, fits each
        spectrum, plots (if requested), and then saves the results.
        """
        if self.data is None:
            self.get_data_dd_single()

        # prepare data for multiprocessing by sorting it into individual dicts
        # note that this process duplicated a lot of data!
        fit_datas = decomp_single_sl._get_fit_datas(self.data)

        # fit
        if(self.data['prep_opts']['nr_cores'] == 1):
            print('single processing')
            # single processing
            results = list(map(decomp_single_sl.fit_one_spectrum, fit_datas))
        else:
            # multi processing
            print('multi processing')
            p = Pool(self.data['prep_opts']['nr_cores'])
            results = p.map(decomp_single_sl.fit_one_spectrum, fit_datas)

        # results now contains one or more ND objects
        self.results = results

    def get_data_dd_single(self):
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
        # make sure we deal with an absolute path
        outdir = os.path.abspath(self.config['output_dir'])

        data, self.config = lDDi.load_frequencies_and_data(self.config)

        # we need list of spectra
        size_y = int(data['raw_data'].shape[1] / 2)
        cr_data = [x.reshape((size_y, 2), order='F') for x in data['raw_data']]

        data['cr_data'] = cr_data

        # we distinguish two sets of options:
        # prep_opts : all settings we need to prepare the inversion (i.e. set
        #             regularization objects)
        # inv_opts : options that are directly looped through to the NDimInv
        # object
        prep_opts, inv_opts = self.config.split_options()

        data['outdir'] = outdir
        data['options'] = self.config
        data['prep_opts'] = prep_opts
        data['inv_opts'] = inv_opts

        self.data = data
        return data
