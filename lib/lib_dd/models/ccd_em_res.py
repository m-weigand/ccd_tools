"""Cole-Cole decomposition in resistivity formulation, including a
high-frequency EM Cole-Cole term
"""
import numpy as np

import NDimInv.plot_helper
plt, mpl = NDimInv.plot_helper.setup()
import NDimInv.model_template as mt
import lib_dd.base_class as base_class
import lib_dd.starting_parameters as starting_parameters
import lib_dd.plot_stats as plot_stats

# import resistivity formulation
import sip_models.res.cc as cc_res


class decomposition_em_resistivity(
    plot_stats._plot_stats,
    base_class.integrated_parameters,
    starting_parameters.starting_parameters,
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
        """ Set the settings and call necessary functions
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
        r"""Convert parameters given as (:math:`\rho_0, m_i`) to the
        parameterization used by this class.
        """
        pars_converted = np.empty_like(pars)
        pars_converted[:] = np.log10(pars[:])
        return pars_converted

    def convert_pars_back(self, pars):
        r"""Convert parameters given in this parameterization back to the
        linear state

        Here: From :math:`log_{10}(\rho_0), log_{10}(m_i)`
        """
        pars_converted = np.empty_like(pars)
        pars_converted[:] = 10 ** pars[:]
        return pars_converted

    def _get_full_pars(self, pars_dec):
        """convert the parameters to linear scale and return full Cole-Cole
        parameters sets (in contrast to the reduced decomposition parameter
        set)
        """
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
        """Forward response of this model

        Parameters
        ----------
        pars_dec: list
            [log10(rho0), log10(m_i), m_m, tau_em, c_em], with m_i a vector of
            the chargabilities

        Returns
        -------

        remim: Nx2 numpy.ndarray
            array with N the nr of frequencies, and the real and the negative
            imaginary parts on the second axis

        """
        pars = self._get_full_pars(pars_dec)
        response = self.cc.response(pars)

        remim = response.rre_rim
        remim[:, 1] *= -1
        return remim

    def Jacobian(self, pars_dec):
        """
        Parameters
        ----------
        pars_dec: numpy.ndarray
            array containing (log10(rho0), log10(m_i)

        Returns
        -------
        J: (2N) X K array with derivatives.
        """
        pars = self._get_full_pars(pars_dec)

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
        """ Return a dict with a description of the data base dimensions. In
        this case we have frequencies and re/im data
        """
        if(self.D_base_dims is None):
            self.D_base_dims = {
                0: ['frequency', self.frequencies.size],
                1: ['rre_rmim', 2],
            }
        return self.D_base_dims

    def get_data_base_size(self):
        """ Return size of flattened base dimensions
        """
        return self.frequencies.size * 2

    def get_model_base_dimensions(self):
        """ Return a dict with a description of the model base dimensions. In
        this case we have one dimension: the DD parameters (rho0, mi) where m_i
        denotes all chargeability values corresponding to the relaxation times.
        """
        M_base_dims = {
            0: ['rho0_mi', self.tau.size + 1]
        }
        return M_base_dims
