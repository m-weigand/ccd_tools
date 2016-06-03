#!/usr/bin/python
"""Cole-Cole decomposition in resistivities
"""
from NDimInv.plot_helper import *
import os
import numpy as np
import NDimInv.model_template as mt
import lib_dd.base_class
# import resistivity
import sip_models.res.cc as cc_res


class decomposition_resistivity(lib_dd.base_class.integrated_parameters,
                                mt.model_template):

    def __init__(self, settings):
        self.data_format = 'rre_rmim'
        self.D_base_dims = None
        required_keys = ('Nd', 'tausel', 'frequencies', 'c')
        for key in required_keys:
            if key not in settings:
                raise Exception('required key not found: {0}'.format(key))

        self.frequencies = settings['frequencies']
        self.set_settings(settings)
        self.cc = cc_res.cc(self.settings['frequencies'])
        self.set_settings(settings)

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

    def convert_parameters(self, pars):
        r"""
        Convert parameters given as (:math:`\rho_0, m_i`) to the
        parameterisation used by this class.
        """
        pars_converted = np.empty_like(pars)
        pars_converted[:] = np.log10(pars[:])
        return pars_converted

    def convert_pars_back(self, pars):
        r"""
        Convert parameters given in this parameterisation back to the linear
        state
        Here: From :math:`log_{10}(\rho_0), log_{10}(m_i)`
        """
        pars_converted = np.empty_like(pars)
        pars_converted[:] = 10 ** pars[:]
        return pars_converted

    def determine_tau_range(self, settings):
        """Return the tau values depending on the settings 'Nd', 'tau_values'
        and 'tau_sel' in the dict 'settings'

        Tau values can be set by using one of the following strings in
            self.settings['tausel']:

                data
                data_ext
                factor_left,factor_right
                ,factor_right
                factor_left,

        Missing values are replaced by one (i.e. the data frequency limits are
                                            used).
        """
        # check which selection strategy to use
        if('tau_values' in settings):
            # we got custom tau values
            tau = settings['tau_values']
            s = np.log10(tau)
            tau_f_values = 1 / (2 * np.pi * tau)
        else:
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
                    raise Exception('Wrong format for tausel')

                if(not items[0]):
                    factor_left = 1
                else:
                    factor_left = int(items[0])

                if(not items[1]):
                    factor_right = 1
                else:
                    factor_right = int(items[1])

            # determine tau values for one data set
            tau, s, tau_f_values = self.get_tau_values_for_data(
                self.settings['Nd'], factor_left=factor_left,
                factor_right=factor_right)
        return tau, s, tau_f_values

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

    def _get_full_pars(self, pars_dec):
        # prepare Cole-Cole parameters
        rho0 = 10**pars_dec[0][np.newaxis]
        m = 10 ** pars_dec[1:]
        tau = self.tau
        if m.size != tau.size:
            raise Exception('m and tau have different sizes!')

        c = np.ones_like(m) * self.settings['c']

        pars = np.hstack((rho0, m, tau, c))
        return pars


    def forward(self, pars_dec):
        """

        Parameters
        ----------
        pars_dec: [log10(rho0),
                   log10(m_i)]

        Returns
        -------

        remim: Nx2 array with N the nr of frequencies, and the real and the
               negative imaginary parts on the second axis

        """
        pars = self._get_full_pars(pars_dec)
        response = self.cc.response(pars)

        remim = response.rre_rim
        remim[:, 1] *= -1
        return remim

    def Jacobian(self, pars_dec):
        """
        Input parameters
        ----------------
        pars_dec: np array containing (log10(rho0), log10(m_i)

        Returns
        -------
        J: (2N) X K array with derivatives.
        """
        pars = self._get_full_pars(pars_dec)
        partials = []

        # real part
        real_J = np.concatenate(
            (
                self.cc.dre_dlog10rho0(pars)[:, np.newaxis],
                self.cc.dre_dlog10m(pars)
            ),
            axis=1
        )
        imag_J = -np.concatenate(
            (
                self.cc.dim_dlog10rho0(pars)[:, np.newaxis],
                self.cc.dim_dlog10m(pars)
            ),
            axis=1
        )
        J = np.concatenate((real_J, imag_J), axis=0).squeeze()
        return J

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

    def estimate_starting_parameters_3(self, re, mim):
        estimator = lib_dd.base_class.starting_pars_3(re, mim, self.frequencies, self.tau)
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
            tre_tmim = self.forward(pars)
            tre = tre_tmim[:, 0]
            tmim = tre_tmim[:, 1]

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

    def estimate_starting_parameters(self, spectrum):
        re = spectrum[:, 0]
        mim = spectrum[:, 1]

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
        rre_rim = self.forward(pars)
        rre = rre_rim[:, 0]
        rmim = -rre_rim[:, 1]

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
