""" Template class for models
"""
import numpy as np

import lib_dd.base_class as base_class
import NDimInv.model_template as mt
import lib_dd.starting_parameters as starting_parameters
import lib_dd.plot_stats as plot_stats


class dd_conductivity(
    plot_stats._plot_stats,
    base_class.integrated_parameters,    # base_class.dd_resistivity_skeleton
    starting_parameters.starting_parameters,
    mt.model_template,
):

    def __init__(self, settings):
        self.data_format = 'cre_cim'
        self.D_base_dims = None
        # required_keys = ('Nd', 'tausel', 'frequencies', 'c')
        required_keys = ('Nd', 'tausel', 'frequencies', )
        for key in required_keys:
            if key not in settings:
                raise Exception('required key not found: {0}'.format(key))

        self.frequencies = settings['frequencies']
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

        self.tau, self.s, self.tau_f_values = base_class.determine_tau_range(
            settings
        )

    def convert_parameters(self, pars):
        """Convert from linear to the actually used scale
        """
        return np.log10(pars.copy())

    def convert_pars_back(self, pars):
        """Convert from log10 to linear
        """
        return 10**pars.copy()

    def forward(self, pars):
        """Return the forward response in base dimensions

        Parameters
        ----------
        pars: [log10(sigma_infty), log10(m_i)]

        Returns
        -------
        response: Nx2 array, first axis denotes frequencies, seconds real and
                  imaginary parts
        """
        # pars = log10(sigma_0), log10(m_i)
        # sigma0 = 10**pars[0]
        m = 10**pars[1:]
        nan_indices = np.where(np.isnan(m))
        m[nan_indices] = 0

        # mtot = np.sum(m)
        # sigmai = sigma0 / (1 - mtot)
        sigmai = 10**pars[0]
        relterms = np.array([mi / (1 + 1j * self.omega * taui) for
                             mi, taui in zip(m, self.tau)])
        response_complex = sigmai * (1 - np.sum(relterms, axis=0))
        response = np.vstack((np.real(response_complex),
                              np.imag(response_complex))).T
        return response

    """
    def forward_re_mim(self, pars):
        response = self.forward(pars)
        return response[0, :], response[1, :]
    """

    def Jacobian(self, pars):
        r"""Return the Jacobian corresponding to the forward response. The
        Jacobian has the dimensions :math:`B \times D \times M`

        TODO: Check the return dimensions
        """
        # sigma0 = 10**pars[0]
        m = 10**pars[1:]
        # mtot = np.sum(m)
        # sigmai = sigma0 / (1 - mtot)
        sigmai = 10**pars[0]

        # compute 1 / (1 + omega^2 tau^2)
        relterms = np.zeros((self.tau.size, self.omega.size))
        for nr1, omega in enumerate(self.omega):
            for nr2, tau in enumerate(self.tau):
                relterms[nr2, nr1] = 1.0 / (1.0 + omega**2 * tau**2)
        # relterms2 = np.array([1 / (1 + self.omega**2 * taui**2) for
        #                      mi, taui in zip(m, self.tau)])

        del_cre_dsigi = np.zeros(self.omega.size)
        for nr, omega in enumerate(self.omega):
            for nr2, mi in enumerate(m):
                taui = self.tau[nr2]
                del_cre_dsigi[nr] += (mi / (1 + omega**2 * taui**2))
        del_cre_dsigi = 1 - del_cre_dsigi

        # del_cre_dsigi = (1 - np.sum(m[:, np.newaxis] * relterms, axis=0))
        del_cre_dsigi *= sigmai

        del_cre_dmi = - sigmai * relterms
        del_cre_dmi *= m[:, np.newaxis]

        # omegatau = np.array([omega * taui for mi, taui in zip(m, self.tau)])
        # omegatau = self.omega[np.newaxis, :] * self.tau[:, np.newaxis]
        # del_cim_dsigi1 = np.sum(omegatau * m[:, np.newaxis] * relterms,
        #                         axis=0)
        del_cim_dsigi = np.zeros(self.omega.size)
        for mi, taui in zip(m, self.tau):
            del_cim_dsigi += (mi * self.omega * taui) / (
                1 + self.omega**2 * taui**2)

        del_cim_dsigi *= sigmai

        # del_cim_dmi1 = sigmai * omegatau / relterms
        del_cim_dmi = np.zeros((self.tau.size, self.omega.size))
        for nr1, omega in enumerate(self.omega):
            for nr2, taui in enumerate(self.tau):
                mi = m[nr2]
                del_cim_dmi[nr2, nr1] = sigmai * omega * taui / (
                    1 + omega**2 * taui**2)

        del_cim_dmi *= m[:, np.newaxis]

        J_re = np.vstack((del_cre_dsigi[np.newaxis, :],
                          del_cre_dmi)).T
        J_im = np.vstack((del_cim_dsigi[np.newaxis, :],
                          del_cim_dmi)).T
        J = np.vstack((J_re, J_im))
        J *= np.log(10)
        return J

    def get_data_base_size(self):
        """Usually you do not need to modify this.
        """
        size = sum([x[1][1] for x in
                    self.get_data_base_dimensions().items()])
        return size

    def get_data_base_dimensions(self):
        """
        Returns
        -------
        Return a dict with a description of the data base dimensions. In this
        case we have frequencies and re/im data
        """
        D_base_dims = {0: ['frequency', self.frequencies.size],
                       1: ['cre_cmim', 2]
                       }
        return D_base_dims

    def get_model_base_dimensions(self):
        """Return a dict with a description of the model base dimensions. In
        this case we have one dimension: the DD parameters (rho0, mi) where m_i
        denotes all chargeability values corresponding to the relaxation times.
        """
        M_base_dims = {0: ['sigi_mi', self.tau.size + 1]}
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
            """Compute :math:`sigma0` using math:`\sigma_\infty` and
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
            """
            Compute the conductivity mtotn:

            .. math::

                m_{tot}^n = \frac{m_{tot}}{\sigma_0}

            """
            mtotn = stat_pars['m_tot'] - stat_pars['rho0']
            return mtotn

        self.stat_pars['m_tot_n'] = mtotn(pars, self.tau, self.s,
                                          self.stat_pars)
        return self.stat_pars
