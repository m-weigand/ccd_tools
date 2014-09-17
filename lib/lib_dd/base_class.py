# from NDimInv.plot_helper import *
from crlab_py.mpl import *
import logging
import numpy as np
import scipy.stats as stats
import os
import Jacobian
import dd_res_data_log10re_mim
import int_pars

logger = logging.getLogger('lib_dd.main')


class starting_pars_3():
    def __init__(self, re, mim, frequencies, taus):
        self.re = re
        self.mim = mim
        self.frequencies = frequencies
        self.tau = taus

        # rho0 can be approximated by the low-frequency magnitude
        self.rho0 = np.sqrt(re[0] ** 2 + mim[0] ** 2)

        # compute bins for each frequency decade
        self.minf = self.frequencies.min()
        self.maxf = self.frequencies.max()

        # round to nearest decade below/above min/max-f
        self.minbin = np.floor(np.log10(self.minf))
        self.maxbin = np.ceil(np.log10(self.maxf))

        # just to be sure, determine tau ranges outside the frequency-derived
        # limits
        self.tau_min = self.tau.min()
        self.tau_max = self.tau.max()
        self.f_tau_min = 1 / (2 * np.pi * self.tau_max)
        self.f_tau_max = 1 / (2 * np.pi * self.tau_min)

        # round to nearest decade below/above
        self.min_tau_bin = np.floor(np.log10(self.f_tau_min))
        self.max_tau_bin = np.ceil(np.log10(self.f_tau_max))

        # determine limits: we only work on the data range
        if(self.min_tau_bin < self.minbin):
            self.min_tau_bin_fl = self.minbin
        else:
            self.min_tau_bin_fl = None
        if(self.max_tau_bin >= self.maxbin):
            self.max_tau_bin_fl = self.maxbin
        else:
            self.max_tau_bin_fl = None

    def get_bins(self):
        # now we compute the frequency bins
        if(self.min_tau_bin_fl is None):
            self.bins_tau_lowf = None
        else:
            self.bins_tau_lowf = np.logspace(self.min_tau_bin, self.minbin,
                                             (self.minbin - self.min_tau_bin)
                                             + 1)
        self.bins_inside_f = np.logspace(self.minbin, self.maxbin,
                                         (self.maxbin - self.minbin) + 1)
        if(self.max_tau_bin_fl is None):
            self.bins_tau_highf = None
        else:
            self.bins_tau_highf = np.logspace(self.maxbin, self.max_tau_bin,
                                              (self.max_tau_bin - self.maxbin)
                                              + 1)

    def get_sec_data(self):
        sec_data = {}
        for key, bins, frequencies in (
                ('lowf', self.bins_tau_lowf, None),
                ('inside', self.bins_inside_f, self.frequencies),
                ('highf', self.bins_tau_highf, None),
                ):
            if(bins is None):
                continue

            # take logarithmic means of frequency data for the bins
            f_logmeans = (np.log10(bins[0:-1]) +
                          np.log10(bins[1:])) / 2

            if(frequencies is not None):
                # assign data points to bins
                data_in_f_bins = np.digitize(frequencies, bins)

                # now avarage the data points for each bin
                f_data_means = []
                fbins = []
                f_f_means = []

                for nr, bin_nr in enumerate(range(1, self.bins_inside_f.size)):
                    f_indices = np.where(data_in_f_bins == bin_nr)[0]
                    # bin_frequencies = frequencies[f_indices]
                    f_data = self.mim[f_indices]
                    f_data_mean = np.mean(f_data)
                    # DD can only handle negative imaginary parts, therefore
                    # replace all positive mim (minus imaginary) values by
                    # data_mean_tau
                    if(f_data_mean <= 0):
                        f_data_mean = self.data_mean_tau
                    # print 'f_data_mean', f_data_mean

                    f_data_means.append(f_data_mean)
                    fbins.append((bins[bin_nr - 1], bins[bin_nr]))
                    f_f_means.append(f_logmeans[nr])

                    outstr = 'The frequencies {0} belong into bin {1} - '
                    outstr += '{2} with mean {3} and flogmean {4}'
                    # print(outstr.format(
                    #   bin_frequencies, fbins[-1][0], fbins[-1][1],
                    #    f_data_mean,
                    #    f_logmeans[nr]))
            else:
                f_data_means = [self.data_mean_tau for x in f_logmeans]
            sec_data[key] = (f_logmeans, f_data_means, bins)
        return sec_data

    def estimate(self, obj):
        """
        Determine a starting model by creating frequency-decade wise mean
        values of mim and then computing a fixed chargeability value for each
        frequency decade.
        """
        # print('Start determining initial parameters')

        # print 'summary'
        #  print 'data un-determined tau range min: {0} - {1}'.format(
        #     min_tau_bin, min_tau_bin_fl)
        # print 'data determined tau range min: {0} - {1}'.format(
        #     minbin, maxbin)
        # print 'data un-determined tau range max: {0} - {1}'.format(
        #     max_tau_bin_fl, max_tau_bin)

        # compute bins
        self.get_bins()

        # the value which will be assigned to tau-range outside the data range
        self.data_mean_tau = self.mim[np.where(self.mim > 0)].min()

        sec_data = self.get_sec_data()

        # select chargeabilities for the frequency decades
        chargeabilities = np.empty_like(self.tau) * np.nan
        ersatz = 0
        for key in sec_data.keys():
            # select tau values corresponding to bins
            tau_bins = 1 / (2 * np.pi * sec_data[key][2])
            tau_digi = np.digitize(self.tau, tau_bins)
            for nr, bin_nr in enumerate(range(1, tau_bins.size)):
                # print 'check for bin nr', bin_nr
                tau_indices = np.where(tau_digi == bin_nr)[0]
                # compute the chargeability for this tau span
                m_dec = (- sec_data[key][1][nr] / self.rho0)
                term = 1
                for i in tau_indices:
                    w = 2 * np.pi * sec_data[key][1][nr]
                    term += 1 / (w * self.tau[i] /
                                 (1 + (w * self.tau[i]) ** 2))
                m_dec *= term
                # print 'm_dec', m_dec

                chargeabilities[tau_indices] = sec_data[key][1][nr]
                ersatz += 1

        # test various scaling factors
        mim_list = []
        rms_list = []
        m_list = []
        scales = np.logspace(-5, 0, 10)
        for scale in scales:
            # test forward modelling
            m_list.append(chargeabilities * scale)
            pars_linear = np.hstack((self.rho0, chargeabilities * scale))
            pars = obj.convert_parameters(pars_linear)
            # print pars
            re_f, mim_f = obj.forward_re_mim(pars)
            # print re_f, mim_f
            mim_list.append(mim_f)
            # compute rms_mim
            rms_mim = np.sqrt((1.0 / float(self.mim.size)) *
                              np.sum(np.abs(mim_f - self.mim) ** 2))
            rms_list.append(rms_mim)
        rms_list = np.array(rms_list)

        # find minimum rms
        min_index = np.argmin(rms_list)

        # select three values
        # indices = [0, min_index, len(scales) - 1]
        indices = [min_index - 1, min_index, min_index + 1]
        # fit parabola to rms-values
        # fit parabola
        x = np.array(scales)[indices]
        y = np.array(rms_list)[indices]

        A = np.zeros((3, 3), dtype=np.float)
        A[:, 0] = x ** 2
        A[:, 1] = x
        A[:, 2] = 1
        a, b, c = np.linalg.solve(A, y)

        # compute minum minmum
        x_min = -b / (2 * a)

        plot_starting_model = False
        if(plot_starting_model):
            # # plot
            fig, axes = plt.subplots(3, 1, figsize=(6, 6))
            # plot spectrum
            # pars_linear = np.hstack((rho0, chargeabilities * x_min))
            pars_linear = np.hstack((self.rho0, chargeabilities * x_min))
            # print 'pars_linear', pars_linear
            pars = obj.convert_parameters(pars_linear)
            re_f, mim_f = obj.forward_re_mim(pars)
            ax = axes[0]
            for key in sec_data.keys():
                ax.scatter(10 ** np.array(sec_data[key][0]), sec_data[key][1],
                           s=30, color='blue')
            ax.loglog(self.frequencies, self.mim, '.-', color='k', alpha=0.5)
            # for scaled_mim in mim_list:
            # print('mimf', mim_f)
            ax.loglog(self.frequencies, mim_f, '-', color='green')
            ax.set_xlim([self.f_tau_min, self.f_tau_max])
            # plot RTD
            ax = axes[1]
            ax.loglog(self.tau, chargeabilities, '.-')

            ax.set_xlim([self.tau.min(), self.tau.max()])
            ax.invert_xaxis()

            # scales vs. rms_mim
            ax = axes[2]
            # print 'scales', scales
            if(not np.all(np.isnan(rms_list))):
                # print 'rms_list', rms_list
                ax.loglog(scales, rms_list, '.-')
                ax.loglog(scales, a * (scales ** 2) + b * scales + c, '-',
                          color='r')
                ax.scatter(scales[indices], rms_list[indices], color='c', s=30)
            fig.savefig('starting_pars3.png', dpi=300)
            plt.close(fig)
            del(fig)
        # print('End determining initial parameters')

        return pars


class integrated_parameters():
    """
    Computation of integrated paramters. This class is not meant to be used
    alone, it is meant to be inherited by 'dd_resistivity_skeleton'
    """

    def compute_par_stats(self, pars):
        r"""
        For a given parameter set (i.e. a fit result), compute relevant
        statistical values such das :math:`m_{tot}`, :math:`m_{tot}^n`,
        :math:`\tau_{50}`, :math:`\tau_{mean}`, :math:`\tau_{peak}`

        Store in self.stat_pars = dict()
        """
        # integrated parameters are computed from the tau/chargeability values
        # corresponding to the data frequency ranges. Therefore we first create
        # linear representation of these values

        # mask all tau values outside the data ranges
        tau_extra_min = np.where(self.tau < self.tau_data_min)[0]
        tau_extra_max = np.where(self.tau > self.tau_data_max)[0]

        # work with linear parameters
        pars_lin = self.convert_pars_back(pars)

        pars_data = np.delete(pars_lin, tau_extra_max + 1)
        pars_data = np.delete(pars_data, tau_extra_min + 1)

        tau_data = self.tau.copy()
        tau_data = np.delete(tau_data, tau_extra_max)
        tau_data = np.delete(tau_data, tau_extra_min)
        s_data = np.log10(tau_data)

        # now compute the integrated parameters
        stat_pars = {}

        # the exception: we want to save the 'raw' pars, tau
        stat_pars['m_i'] = np.log10(pars_lin[1:])

        # coverages are computed on the whole parameter range
        covm, covf = self._compute_coverages(pars)
        stat_pars['covm'] = covm
        stat_pars['covf'] = covf

        # "regular" integrated pars
        int_par_keys = {'rho0': int_pars.rho0,
                        'm_data': int_pars.m_data,
                        'm_tot': int_pars.m_tot,
                        'm_tot_n': int_pars.m_tot_n,
                        'tau_x': int_pars.tau_x,
                        'tau_50': int_pars.tau_50,
                        'tau_mean': int_pars.tau_mean,
                        'tau_peaks': int_pars.tau_peaks,
                        'tau_max': int_pars.tau_max,
                        'U_tau': int_pars.U_tau,
                        'tau_arithmetic': int_pars.tau_arithmetic,
                        'tau_geometric': int_pars.tau_geometric,
                        'decade_loadings': int_pars.decade_loadings
                        }
        for key, func in int_par_keys.iteritems():
            result = func(pars_data, tau_data, s_data)
            if(isinstance(result, dict)):
                stat_pars.update(result)
            else:
                stat_pars[key] = result

        self.stat_pars = stat_pars
        return self.stat_pars

    def _compute_coverages(self, pars):
        """

        """
        Jacobian = self.Jacobian(pars)
        Jsize = Jacobian.shape

        # extract dsigma''/dm
        del_mim_del_m = Jacobian[Jsize[0] / 2:, 1:]

        covf = np.abs(del_mim_del_m).sum(axis=1)
        covf /= np.max(covf)

        covm = np.abs(del_mim_del_m).sum(axis=0)
        covm /= np.max(covm)
        return covm, covf


class dd_resistivity_skeleton(
        dd_res_data_log10re_mim.add_log10re_mim_derivatives,
        integrated_parameters):
    """
    Required keys for the 'settings' struct:
        Nd
        frequencies
        tausel
    """
    def __init__(self, settings):
        # set the data format we work with.
        self.data_format = 'rre_rmim'
        self.set_settings(settings)
        self.D_base_dims = None
        self.D_dims_flat = None  # size of the flattened base dimensions

    def set_settings(self, settings):
        """
        Set the settings and call necessary functions
        """
        self.settings = settings

        # extract some variables
        self.frequencies = self.settings['frequencies']
        self.omega = 2.0 * np.pi * self.frequencies

        # set min/max tau values corresponding to data limits
        self.tau_data_min = 1 / (2 * np.pi * self.frequencies.max())
        self.tau_data_max = 1 / (2 * np.pi * self.frequencies.min())

        self.tau, self.s, self.tau_f_values = self.determine_tau_range(settings)

    def determine_tau_range(self, settings):
        """
        Return the tau values depending on the settings 'Nd', 'tau_values' and
        'tau_sel' in the dict 'settings'
        """
        # check which selection strategy to use
        if('tau_values' in settings):
            # we got custom tau values
            tau = settings['tau_values']
            s = np.log10(tau)
            tau_f_values = 1 / (2 * np.pi * tau)
        else:
            """
            Tau values can be set by using one of the following strings in
            self.settings['tausel']:

                data
                data_ext
                factor_left,factor_right
                ,factor_right
                factor_left,

            Missing values are replaced by one (i.e. the data frequency limits
            are used).
            """
            # determine range
            if(self.settings['tausel'] == 'data'):
                    factor_left = 1
                    factor_right = 1
            elif(self.settings['tausel'] == 'data_ext'):
                    factor_left = 10
                    factor_right = 10
            else:
                # try to parse
                items = self.settings['tausel'].split(',')
                if(len(items) != 2):
                    raise IOError('Wrong format for tausel')

                if(not items[0]):
                    factor_left = 1
                else:
                    factor_left = int(items[0])

                if(not items[1]):
                    factor_right = 1
                else:
                    factor_right = int(items[1])

            logger.debug('Tau range factors', factor_left, factor_right)
            # determine tau values for one data set
            tau, s, tau_f_values = self.get_tau_values_for_data(
                self.settings['Nd'], factor_left=factor_left,
                factor_right=factor_right)
        return tau, s, tau_f_values

    def get_data_base_dimensions(self):
        """
        Return a dict with a description of the data base dimensions. In this
        case we have frequencies and re/im data
        """
        if(self.D_base_dims is None):
            self.D_base_dims = {0: ['frequency', self.frequencies.size],
                                1: ['rre_rmim', 2]
                                }
        return self.D_base_dims

    def get_data_base_size(self):
        """
        Return size of flattened base dimensions
        """
        return self.frequencies.size * 2

    def get_model_base_dimensions(self):
        """
        Return a dict with a description of the model base dimensions. In this
        case we have one dimension: the DD parameters (rho0, mi) where m_i
        denotes all chargeability values corresponding to the relaxation times.
        """
        M_base_dims = {0: ['rho0_mi', self.tau.size + 1]
                       }
        return M_base_dims

    def get_tau_values_for_data(self, Nd, factor_left=1,
                                factor_right=1):
        r"""
        Return the :math:`\tau` values corresponding to the frequency range of
        the data set.

        Parameters
        ----------
        Nd : number of :math:`\tau` values per decade
        factor_left : factor to divide to the lower limit by
        factor_right : factor to multiply to the upper limit

        Returns
        -------
        tau,s with :math:`s = log_{10}(\tau)`

        """
        frequencies = self.frequencies

        minf = np.min(frequencies)
        maxf = np.max(frequencies)

        # check min/max frequencies
        # if(minf < 1e-4):
        #    logger.warn('Minimum frequency below global minimum')

        # if(maxf > 1e-4):
        #    logger.warn('Maximum frequency above global minimum')

        # global min/max values for tau, corresponding to the frequency range
        # [1e-4 Hz,1e6 Hz]
        min_tau_f = 1e-15
        max_tau_f = 1e16
        nr_decades = np.log10(max_tau_f) - np.log10(min_tau_f)
        g_tau_fmin = 1.0 / (2 * np.pi * 1e-15)
        g_tau_fmax = 1.0 / (2 * np.pi * 1e16)

        # compile total pool of tau values
        # the (fixed) global frequency range spans 9 order of magnitude
        N = nr_decades * Nd
        g_tau = np.logspace(np.log10(g_tau_fmin), np.log10(g_tau_fmax), N)
        g_tau_frequencies = 1.0 / (2 * np.pi * g_tau)

        # the global pool
        g_pool = np.hstack((g_tau_frequencies[:, np.newaxis],
                            g_tau[:, np.newaxis]))

        # find nearest index
        fmin = minf / float(factor_left)
        fmax = maxf * float(factor_right)

        index_min = np.argmin(np.abs(g_pool[:, 0] - fmin))
        index_max = np.argmin(np.abs(g_pool[:, 0] - fmax))

        # fmin/fmax depend on the data frequency range
        # when we choose our tau value out of the (data independent) pool, it
        # is possible that we choose a tau value corresponding to a slightly
        # larger/smaller value of fmin/max. In those cases we just use the next
        # smaller/larger value of tau
        if(g_pool[index_min, 0] > fmin and index_min > 0):
            # logger.info('Reducing index_min by one')
            index_min -= 1

        if(g_pool[index_max, -1] < fmax and index_max < (g_pool.shape[0] - 1)):
            # logger.info('Increasing index_max by one')
            index_max += 1

        tau_data = g_pool[index_min:index_max + 1, :]

        # tau values should be sorted in ascending order
        if(tau_data[0, 1] > tau_data[-1, 1]):
            tau_data = tau_data[::-1, :]

        tau_s = tau_data[:, 1]
        f_s = tau_data[:, 0]
        s_s = np.log10(tau_s)

        return tau_s, s_s, f_s

    def estimate_starting_parameters_3(self, re, mim):
        estimator = starting_pars_3(re, mim, self.frequencies, self.tau)
        parameters = estimator.estimate(self)
        return parameters

    def estimate_starting_parameters_2(self, re, mim):
        """
        Try to find good starting parameters using a gaussian m-distribution.

        This should only work well if we have only one peak in the data
        (imaginary/phase)
        """
        rho0 = np.sqrt(re[0] ** 2 + mim[0] ** 2)

        # start playing with gaussians distributions
        pol_maximum = np.argmax(mim)

        f_max = self.frequencies[pol_maximum]
        tau_max = 1 / (2 * np.pi * f_max)
        s_max = np.log10(tau_max)

        m = stats.norm.pdf(self.s, s_max, 1)
        # normalize
        m /= np.sum(m)

        pars_linear = np.hstack((rho0, m))
        parameters = self.convert_parameters(pars_linear)
        return parameters

    def estimate_starting_parameters_1(self, re, mim):
        """
        Heuristic 1 to generate a suitable starting distribution for a fit

        TODO: Florsch et al. 2014 has a name for this kind of heuristic...
        """
        parameters = np.zeros((self.s.shape[0] + 1))
        pars = np.zeros(parameters.shape)

        # rho0
        parameters[0] = np.sqrt(re[0] ** 2 + mim[0] ** 2)

        # generate test chargeabilities m_i
        test_m = np.logspace(-12, 0, 20)

        best = 0
        best_diff = None
        for nr, i in enumerate(test_m):
            pars[0] = parameters[0]
            pars[1:] = i
            pars = self.convert_parameters(pars)
            tre, tmim = self.forward_re_mim(pars)

            diff_im = np.sum(np.abs(tmim - mim))
            if(best_diff is None or best_diff > diff_im):
                best_diff = diff_im
                best = nr
            if('DD_DEBUG_STARTING_PARS' in os.environ and
               os.environ['DD_DEBUG_STARTING_PARS'] == '1'):
                # enable debug plots
                fig, axes = plt.subplots(2, 1, figsize=(5, 4))
                fig.suptitle('test m: {0} - diff\_im: {1}'.format(
                    i, diff_im))
                ax = axes[0]
                ax.semilogx(self.frequencies, re, '.-', color='k')
                ax.semilogx(self.frequencies, tre, '.-', color='gray')
                ax.set_ylabel(r'part1')
                ax.set_xlabel('f (Hz)')
                ax = axes[1]
                ax.semilogx(self.frequencies, mim, '.-', color='k')
                ax.semilogx(self.frequencies, tmim, '.-', color='gray')
                ax.set_ylabel(r'part2')
                ax.set_xlabel('f (Hz)')
                filename = 'starting_model_{0}.png'.format(nr)
                fig.savefig(filename, dpi=150)

        parameters[1:] = test_m[best]

        parameters = self.convert_parameters(parameters)
        return parameters

    def estimate_starting_parameters(self, re, mim):
        if('DD_STARTING_MODEL' in os.environ):
            starting_model = os.environ['DD_STARTING_MODEL']
            starting_model = int(starting_model)
        else:
            starting_model = 1

        if(starting_model == 1):
            # find good flat starting paramaters
            parameters = self.estimate_starting_parameters_1(re, mim)
        elif(starting_model == 2):
            # find normally distributed starting parameters
            parameters = self.estimate_starting_parameters_2(re, mim)
        elif(starting_model == 3):
            # frequency bin wise
            parameters = self.estimate_starting_parameters_3(re, mim)

        return parameters

    def get_synthetic_spectrum(self, omega, s, rho0, nr_chargeability,
                               strength=10, noise=0):
        """
        For a given set of frequencies, return re, -im parts of a synthetic
        debye-spectrum
        """
        m = stats.norm.pdf(s, 0, 1.5) * (strength) + \
            stats.norm.pdf(s, -4.5, 1.5) * (strength * 2)

        # we need to norm the chargeabilities because they will be scaled by
        # rho0. Arbitrarily set the norm factor so that it is 1 for rho0 = 100
        m = m / rho0
        # 1.0 / (rho0 * m)

        # we also want to normalize to the number
        f = 1 / (2 * np.pi * 10 ** s)
        nr_per_decade = int(nr_chargeability / (np.log10(np.max(f)) -
                                                np.log10(np.min(f))))

        m = m / nr_per_decade

        # apply conversion
        pars = np.hstack((rho0, m))
        pars_converted = self.convert_parameters(pars)
        re, mim = self.forward_re_mim(omega, pars_converted, s)

        if(noise != 0):
            # add noise
            np.random.seed(5)
            re = re + np.random.rand(re.shape[0]) * noise * re
            mim = mim + np.random.rand(mim.shape[0]) * noise * mim

        return pars_converted, re, mim

    def Jacobian_re_mim(self, pars):
        partials = [self.del_re_del_dc, self.del_re_del_chargeability,
                    self.del_mim_del_dc, self.del_mim_del_chargeability]
        return Jacobian.Jacobian(self.omega, pars, self.s, partials)

    def Jacobian(self, pars):
        J = self.Jacobian_re_mim(pars)
        return J

    def plot_stats(self, prefix):
        """
        Plot various statistics. Requires self.stat_pars to be present.
        """
        self._plot_coverages(prefix)

    def _plot_coverages(self, prefix):
        f = self.frequencies
        fig, axes = plt.subplots(2, 2, figsize=(5, 4))
        # plot data/fig
        pars = np.hstack((self.stat_pars['rho0'], self.stat_pars['m_i']))
        rre, rmim = self.forward_re_mim(pars)

        ax = axes[0, 0]
        try:
            ax.semilogx(f, rre, '.-', color='k', label='fit')
        except:
            pass
        ax.set_xlabel('f (Hz)')
        ax.set_ylabel(r"$\rho'$")

        ax = axes[1, 0]
        try:
            ax.semilogx(f, rmim, '.-', color='k', label='fit')
        except:
            pass
        ax.set_xlabel('f (Hz)')
        ax.set_ylabel(r"$\rho''$")

        # plot coverages
        ax = axes[0, 1]
        try:
            ax.semilogx(f, self.stat_pars['covf'], '.-', color='k')
        except:
            pass
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Covf')
        ax.set_xlim([f.min(), f.max()])

        ax = axes[1, 1]
        s = self.s
        try:
            ax.plot(s, self.stat_pars['covm'], '.-', color='k')
        except:
            pass
        ax.set_xlabel(r'$s = log_{10}(\tau)$')
        ax.set_ylabel('Covm')
        ax.set_xlim([s.min(), s.max()])
        ax.invert_xaxis()

        fig.tight_layout()
        outfile = '{0}_coverages_nr.png'.format(prefix)
        fig.savefig(outfile)
        fig.clf()
        plt.close(fig)
        del(fig)

    def check_data(self, rre, mrim):
        """
        We restrict the fit to positive m values. This implies also positive
        imaginary parts!  Reject a data set if the data mean is negative

        Parameters
        ----------
        rre : real part of resistivity/resistance
        rmim : negative of imaginary part of resistivity/resistance

        Returns
        -------
        check_passed : [True|False] Return true of no test applied, return
                       false if the spectrum is not deemed fitable
        """
        check_passed = True

        if(np.mean(mrim) < 0):
            print('Imaginary part mean is negative. Exiting fit')
            check_passed = False

        nr_mim = mrim.shape[0]
        nr_negative_mrim = len(np.where(mrim < 0)[0])
        if(nr_negative_mrim > 0 and nr_mim / nr_negative_mrim <= 2):
            print(
                'Too many negative mim entries: {0} from: {1}'.format(
                    nr_negative_mrim, nr_mim))
            check_passed = False

        return check_passed
