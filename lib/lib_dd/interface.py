"""
Functions common to the Debye implementations dd_single, dd_time,
dd_space_time.
"""
import numpy as np
import sip_formats.convert as SC
# ## general helper functions ###


def aggregate_dicts(iteration_list, dict_name):
    """
    For a given list of NDimInv iterations, aggregate the dictionaries with
    name 'dict_name' (Iteration.dict_name) and return on dict containing the
    values of all iterations as lists.
    """
    global_stat_pars = {}

    keys = getattr(iteration_list[0][0], dict_name).keys()
    # keys = iteration_list[0][0].stat_pars.keys()
    for it, nr in iteration_list:
        adict = getattr(it, dict_name)
        for key in keys:
            value = adict[key]
            # we need lists to aggregate
            if(type(value) is not list):
                value = [value, ]

            if(key not in global_stat_pars):
                global_stat_pars[key] = value
            else:
                global_stat_pars[key] += value
    return global_stat_pars

# ## load functions ###


def _get_frequencies(options):
    if(options.ignore_frequencies is not None):
        f_ignore_ids = [int(x) for x in options.ignore_frequencies.split(',')]
    else:
        f_ignore_ids = None

    frequencies = np.loadtxt(options.frequency_file)
    # filter frequencies
    if(f_ignore_ids is not None):
        frequencies = np.delete(frequencies, f_ignore_ids, axis=0)
    return frequencies, f_ignore_ids


def load_frequencies_and_data(options):
    """
    Load frequencies and data from options.frequency_file and
    options.data_file. Apply certain processing steps such as:

        * frequency filtering
        * magnitude normalization

    Parameters
    ----------
    options: object as created by optparse (e.g. provided by dd_single.py or
             dd_time.py)
    """
    data = {}

    frequencies, f_ignore_ids = _get_frequencies(options)
    data['frequencies'] = frequencies
    # # data ##
    # # load raw data
    try:
        raw_data = np.atleast_2d(np.loadtxt(options.data_file))
    except Exception, e:
        print('There was an error loading the data file')
        print(e)
        exit()

    # # filter frequencies
    if(f_ignore_ids is not None):
        # split data for easy access
        part1 = raw_data[:, 0:raw_data.shape[1] / 2]
        part2 = raw_data[:, raw_data.shape[1] / 2:]
        part1 = np.delete(part1, f_ignore_ids, axis=1)
        part2 = np.delete(part2, f_ignore_ids, axis=1)
        # rebuild raw_data
        raw_data = np.hstack((part1, part2))

    # # apply normalization if necessary
    if(options.norm_mag is not None):
        # data must me in format 'rmag_rpha'
        if(options.data_format != "rmag_rpha"):
            raw_data = SC.convert(options.data_format, 'rmag_rpha', raw_data)
            options.data_format = 'rmag_rpha'

        # apply normalization
        index_end = raw_data.shape[1] / 2
        norm_factors = options.norm_mag / raw_data[:, 0]
        norm_factors = np.resize(norm_factors.T,
                                 (index_end, norm_factors.size)).T
        raw_data[:, 0:index_end] *= norm_factors
        data['norm_factors'] = np.atleast_1d(norm_factors[:, 0].squeeze())

    data['raw_data'] = raw_data
    return data


# ## save functions ###


def save_stat_pars(stat_pars, norm_factors=None):
    """
    Saves to current working directy.
    """
    # get keys of statistical parameters
    keys = stat_pars.keys()

    # save keys (statistics)
    for key in keys:
        raw_values = stat_pars[key]
        # we need to treat some keys different than others before we can save
        # them
        values = prepare_stat_values(raw_values, key, norm_factors)

        filename = '{0}_results.dat'.format(key)
        np.savetxt(filename, np.atleast_1d(values))


def prepare_stat_values(raw_values, key, norm_factors):
    """
    Prepare stat_pars for saving to disc.

    This included renormalization or padding for specific keys.

    Divide the statistical parameter rho0 by norm_factors and multiply m_tot_n
    by them.
    """
    # pad variable length parameters with nan so that we can save them to disc
    # using np.savetxt
    if(key == 'tau_peaks_all' or key == 'f_peaks_all'):
        # first iteration: get max. nr of peaks
        max_len = max([len(x) for x in raw_values])

        def padwithnans(vector, pad_width, iaxis, kwargs):
            # pad with np.nans
            # we need this function to accomplish that, see documentation
            # of np.pad
            if(pad_width[1] == 0):
                return vector
            vector[-pad_width[1]:] = np.nan
            return vector

        values = [np.pad(i, (0, max_len - i.size), padwithnans) for i
                  in raw_values]
    else:
        values = np.array(raw_values)
        values = values.squeeze()

    # renormalize all parameters containing rho0
    if(key == 'rho0' and norm_factors is not None):
        # rho0 is log10
        # renormalize
        values -= np.log10(norm_factors).squeeze()
    if(key == 'm_tot_n' and norm_factors is not None):
        # renormalize
        values += np.log10(norm_factors).squeeze()
        print 'm_tot_n', values

    return values


def save_rms_values(rms_values):
    """
    Save the dict containing all rms values to file
    """
    for key, item in rms_values.iteritems():
        filename = key + '.dat'
        np.savetxt(filename, np.atleast_1d(item))
