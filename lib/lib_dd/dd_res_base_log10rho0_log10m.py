# -*- coding: utf-8 -*-
"""
Copyright 2014 Maximilian Weigand

"""
import logging
import numpy as np
import dd_res_base_rho0_m


class dd_res_base(dd_res_base_rho0_m.dd_res_base):
    r"""
    Provide forward function and derivatives for the Debye-Decomposition using
    the parameterization :math:`(\rho_0, log_{10}(m_i))`
    """
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

    def forward_re(self, pars):
        """
        Real part of debye distribution

        Parameters
        ----------
        pars: (log_10(rho0), log_10(m_i))
        """
        debye_terms = np.zeros(self.omega.shape[0], dtype=np.float64)
        np.seterr(over='raise')

        #logger = logging.getLogger('dd.dd_res')

        for index, rel_time in enumerate(self.s):
            #try:
            term = 10 ** pars[index + 1] * (self.omega * 10 ** rel_time)\
                ** 2 / (1 + (self.omega * 10 ** rel_time) ** 2)
            #except FloatingPointError:
            #    print('Floating Point Error')
                #logger.error('Arithmetic Error')
                #logger.error(pars[index + 1])
                #logger.error(10 ** rel_time)

            debye_terms += term
        debye_terms = 10 ** pars[0] * (1 - debye_terms)
        return (debye_terms)

    def forward_mim(self, pars):
        r"""
        Return :math:`-Im (\rho)`
        """
        debye_terms = np.zeros(self.omega.shape[0], dtype=np.float64)
        for index, rel_time in enumerate(self.s):
            term = 10 ** pars[index + 1] * (self.omega * 10 ** rel_time) /\
                (1 + (self.omega * 10 ** rel_time) ** 2)
            debye_terms += term

        debye_terms = 10 ** pars[0] * debye_terms
        return debye_terms

    def del_re_del_dc(self, pars):
        r"""
        Calculate the derivate :math:`\frac{\partial \underline{Re}}{\partial
        \rho_0}`

        Return an K x 1 vector.
        """
        K = self.omega.shape[0]

        derivative = np.ones((K, 1), dtype=np.float64) *\
            10 ** (pars[0]) * np.log(10)
        for index, rel_time in enumerate(self.s):
            derivative[:, 0] -= np.log(10) * 10 ** pars[0] *\
                (10 ** pars[index + 1] * (self.omega * 10 ** rel_time) ** 2 /
                 (1 + (self.omega * 10 ** rel_time) ** 2))
        return derivative

    def del_re_del_chargeability(self, pars):
        r"""
        Calculate the derivate :math:`\frac{\partial \underline{-Im}}{\partial
        m_i}`

        Return a K x N vector.

        """
        K = self.omega.shape[0]

        derivative = np.ones((K, self.s.shape[0]), dtype=np.float64)

        for column in range(0, self.s.shape[0]):
            derivative[:, column] = -10 ** pars[0] * np.log(10) * 10 **\
                pars[column + 1] * (self.omega * 10 ** self.s[column]) ** 2\
                / (1 + (self.omega * 10 ** self.s[column]) ** 2)

        return derivative

    def del_mim_del_dc(self, pars):
        r"""
        Calculate the derivate :math:`\frac{\partial \underline{-Im}}{\partial
        \rho_0}`

        Return a K x 1 vector.
        """
        K = self.omega.shape[0]

        derivative = np.zeros((K, 1), dtype=np.float64)
        for index, rel_time in enumerate(self.s):
            derivative[:, 0] += (10 ** pars[index + 1] *
                                 (self.omega * 10 ** rel_time) /
                                 (1 + (self.omega * 10 ** rel_time) ** 2))
        derivative[:, 0] *= np.log(10) * 10 ** pars[0]
        return derivative

    def del_mim_del_chargeability(self, pars):
        r"""
        Calculate the derivate :math:`\frac{\partial \underline{-Im}}{\partial
        m_i}`

        Return an K x N vector.

        """
        K = self.omega.shape[0]

        derivative = np.ones((K, self.s.shape[0]), dtype=np.float64)

        for column in range(0, self.s.shape[0]):
            derivative[:, column] = np.log(10) * 10 ** pars[column + 1] *\
                (self.omega * 10 ** self.s[column]) / (1 + (self.omega * 10 **
                                                            self.s[column]) **
                                                       2)

        derivative *= 10 ** pars[0]
        return derivative
