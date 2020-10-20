"""Cole-Cole decomposition in conductivity formulation
"""
import numpy as np

import NDimInv.plot_helper
import NDimInv.model_template as mt
import lib_dd.base_class as base_class
import lib_dd.starting_parameters as starting_parameters
import lib_dd.plot_stats as plot_stats

# import conductivity formulation
import sip_models.cond.cc as cc_cond

plt, mpl = NDimInv.plot_helper.setup()


class decomposition_conductivity(
    plot_stats._plot_stats,
    base_class.integrated_parameters,
    starting_parameters.starting_parameters,
        mt.model_template):

    def __init__(self, settings):
        self.data_format = 'cre_cim'
        self.D_base_dims = None
        required_keys = ('Nd', 'tausel', 'frequencies', 'c')
        for key in required_keys:
            if key not in settings:
                raise Exception('required key not found: {0}'.format(key))

        self.frequencies = settings['frequencies']
        self.set_settings(settings)
        self.cc = cc_cond.cc(self.settings['frequencies'])
        self.set_settings(settings)

    def set_settings(self, settings):
        """ Set the settings and call necessary functions

        Parameters
        ----------
        settings: dict
            contains settings of the decomposition kernel
        """
        self.settings = settings

        # extract some variables
        self.frequencies = self.settings['frequencies']
        self.omega = 2.0 * np.pi * self.frequencies

        # set min/max tau values corresponding to data limits
        self.tau_data_min = 1 / (2 * np.pi * self.frequencies.max())
        self.tau_data_max = 1 / (2 * np.pi * self.frequencies.min())

        self.tau, self.s, self.tau_f_values = base_class.determine_tau_range(
            settings
        )

    def convert_parameters(self, pars):
        r""" Convert parameters given as (:math:`\sigma_\infty, m_i`) to the
        parameterization used by this class.
        """
        pars_converted = np.empty_like(pars)
        pars_converted[:] = np.log10(pars[:])
        return pars_converted

    def convert_pars_back(self, pars):
        r""" Convert parameters given in this parameterization back to the
        linear state
        Here: From :math:`log_{10}(\sigma_\infty), log_{10}(m_i)`
        """
        pars_converted = np.empty_like(pars)
        pars_converted[:] = 10 ** pars[:]
        return pars_converted

    def _get_full_pars(self, pars_dec):
        # prepare Cole-Cole parameters
        sigmai = 10**pars_dec[0][np.newaxis]
        m = 10 ** pars_dec[1:]
        tau = self.tau
        if m.size != tau.size:
            raise Exception('m and tau have different sizes!')

        c = np.ones_like(m) * self.settings['c']

        pars = np.hstack((sigmai, m, tau, c))
        return pars

    def forward(self, pars_dec):
        """Forward response of this model

        Parameters
        ----------
        pars_dec: or numpy.ndarray
            [log10(sigma_infty), log10(m_i)]

        Returns
        -------
        remim: Nx2 numpy.ndarray
            with N the nr of frequencies, and the real and the negative
            imaginary parts on the second axis

        """
        pars = self._get_full_pars(pars_dec)
        response = self.cc.response(pars)

        creim = response.cre_cim
        return creim

    def Jacobian(self, pars_dec):
        """
        Parameters
        ----------
        pars_dec: numpy.ndarray
            array containing (log10(sigma_infty), log10(m_i)

        Returns
        -------
        J: (2N) X K numpy.ndarray
            containing derivatives.
        """
        pars = self._get_full_pars(pars_dec)

        # real part
        real_J = np.concatenate(
            (
                self.cc.dre_dlog10sigmai(pars)[:, np.newaxis],
                self.cc.dre_dlog10m(pars)
            ),
            axis=1
        )
        imag_J = -np.concatenate(
            (
                self.cc.dim_dlog10sigmai(pars)[:, np.newaxis],
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
        if self.D_base_dims is None:
            self.D_base_dims = {
                0: ['frequency', self.frequencies.size],
                1: ['cre_cim', 2]
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
        M_base_dims = {
            0: ['rho0_mi', self.tau.size + 1]
        }
        return M_base_dims

    def compute_par_stats(self, pars):
        r"""For a given parameter set (i.e. a fit result), compute relevant
        statistical values such as :math:`m_{tot}`, :math:`m_{tot}^n`,
        :math:`\tau_{50}`, :math:`\tau_{mean}`, :math:`\tau_{peak}`

        This is the way to compute any secondary results based on the fit
        results.

        Store in self.stat_pars = dict()

        """
        base_class.integrated_parameters.compute_par_stats(self, pars)

        # self.stat_pars = {}
        # the statistical parameters as computed above relate to the
        # resistivity formulation. We must correct some of them and add a few
        # parameters.
        self.stat_pars['sigma_infty'] = self.stat_pars['rho0'].copy()

        def sigma0_linear(pars, tau, s, stat_pars):
            r"""Compute :math:`sigma0` using math:`\sigma_\infty` and
            :math:`m_{tot}`:

            .. math::

                \sigma_0 = \sigma_\infty \cdot (1 - m_{tot})

            """
            sigma0 = 10 ** stat_pars['sigma_infty'] *\
                (1 - 10 ** stat_pars['m_tot'])
            return sigma0

        def sigma0(pars, tau, s, stat_pars):
            return np.log10(sigma0_linear(pars, tau, s, stat_pars))

        self.stat_pars['sigma0'] = sigma0(pars, self.tau, self.s,
                                          self.stat_pars)

        # rho0 is stored in log10, change sign for 1/rho0
        self.stat_pars['rho0'] = self.stat_pars['sigma0'] * -1

        def mtotn(pars, tau, s, stat_pars):
            r"""
            Compute the conductivity mtotn:

            .. math::

                m_{tot}^n = \frac{m_{tot}}{\sigma_0}

            """
            mtotn = stat_pars['m_tot'] - stat_pars['rho0']
            return mtotn

        self.stat_pars['m_tot_n'] = mtotn(pars, self.tau, self.s,
                                          self.stat_pars)
        return self.stat_pars
