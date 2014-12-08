# -*- coding: utf-8 -*-
"""
Copyright 2014 Maximilian Weigand

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import numpy as np


class dd_res_base():
    r"""
    Provide forward function and derivatives for the Debye-Decomposition using
    the parameterization :math:`(\rho_0, m_i)`
    """

    def convert_parameters(self, pars):
        r"""
        Convert parameters given as (:math:`\rho_0, m_i`) to the
        parameterisation used by this class.
        """
        return pars

    def forward(self, pars):
        """
        Return the forward response as in base dimensions
        """
        real, mimag = self.forward_re_mim(pars)
        rre_rmim = np.vstack((real, mimag)).T
        return rre_rmim

    def forward_re_mim(self, pars):
        r"""
        Calculate the response of a debye-distribution.

        Parameters
        ----------
        pars : parameter vector: (rho0, m1, ..., m_N). All parameters are
               linear.

        Returns :math`(Re(\rho)); (-Im(\rho))`
        """
        real = self.forward_re(pars)
        mimag = self.forward_mim(pars)
        return real, mimag

    def forward_log10re_mim(self, pars):
        real = self.forward_log10re(pars)
        mimag = self.forward_mim(pars)
        return real, mimag

    def forward_re(self, pars):
        """
        Real part of debye distribution

        pars = (rho0, m_i)
        """
        debye_terms = np.zeros(self.omega.shape[0], dtype=np.float64)
        np.seterr(over='raise')

        for index, rel_time in enumerate(self.s):
            try:
                term = pars[index + 1] *\
                    (self.omega * 10 ** rel_time) ** 2 /\
                    (1 + (self.omega * 10 ** rel_time) ** 2)
            except FloatingPointError:
                print('Arithmetic Error')
                print(pars[index + 1])
                print(10 ** rel_time)
                exit()

            debye_terms += term
        debye_terms = pars[0] * (1 - debye_terms)
        return (debye_terms)

    def forward_log10re(self, pars):
        """
        Return log10(Re)
        """
        return np.log10(self.forward_re(pars))

    def forward_mim(self, pars):
        r"""
        Return :math:`-Im (\rho)`
        """
        debye_terms = np.zeros(self.omega.shape[0], dtype=np.float64)
        for index, rel_time in enumerate(self.s):
            term = pars[index + 1] *\
                (self.omega * 10 ** rel_time) /\
                (1 + (self.omega * 10 ** rel_time) ** 2)
            debye_terms += term

        debye_terms = pars[0] * debye_terms
        return debye_terms

    def del_re_del_dc(self, pars):
        r"""
        Calculate the derivate :math:`\frac{\partial \underline{Re}}{\partial
        \rho_0}`

        Return an K x 1 vector.
        """
        pars = self.convert_parameters(pars)
        K = self.omega.shape[0]

        derivative = np.ones((K, 1), dtype=np.float64)
        for index, rel_time in enumerate(self.s):
            derivative[:, 0] -= (pars[index + 1] *
                                 (self.omega * 10 ** rel_time) ** 2 /
                                 (1 + (self.omega * 10 ** rel_time) ** 2))
        return derivative

    def del_re_del_chargeability(self, pars):
        r"""
        Calculate the derivate :math:`\frac{\partial \underline{-Im}}{\partial
        m_i}`

        Return an K x N vector.

        """
        pars = self.convert_parameters(pars)
        K = self.omega.shape[0]

        derivative = np.ones((K, self.s.shape[0]), dtype=np.float64)

        for column in range(0, self.s.shape[0]):
            derivative[:, column] = - pars[0] *\
                (self.omega * 10 ** self.s[column]) ** 2 /\
                (1 + (self.omega * 10 ** self.s[column]) ** 2)

        return derivative

    def del_mim_del_dc(self, pars):
        r"""
        Calculate the derivate :math:`\frac{\partial \underline{-Im}}{\partial
        \rho_0}`

        Return an K x 1 vector.
        """
        pars = self.convert_parameters(pars)
        K = self.omega.shape[0]

        derivative = np.zeros((K, 1), dtype=np.float64)
        for index, rel_time in enumerate(self.s):
            derivative[:, 0] += (pars[index + 1] *
                                 (self.omega * 10 ** rel_time) /
                                 (1 + (self.omega * 10 ** rel_time) ** 2))
        return derivative

    def del_mim_del_chargeability(self, pars):
        r"""
        Calculate the derivate :math:`\frac{\partial \underline{-Im}}{\partial
        m_i}`

        Return an K x N vector.

        """
        pars = self.convert_parameters(pars)
        K = self.omega.shape[0]

        derivative = np.ones((K, self.s.shape[0]), dtype=np.float64)

        for column in range(0, self.s.shape[0]):
            derivative[:, column] = (self.omega * 10 ** self.s[column]) /\
                (1 + (self.omega * 10 ** self.s[column]) ** 2)

        derivative *= pars[0]
        return derivative

    def del_log10re_del_dc(self, pars):
        r"""
        Calculate the derivate :math:`\frac{\partial
        log_{10}(\underline{Re})}{\partial \rho_0}`

        Return an K x 1 vector.
        """
        pars = self.convert_parameters(pars)
        re = self.forward_re(pars)
        dre_drho0_linear = self.del_re_del_rho0(pars)

        derivative = 1 / np.log(10) * (1 / re)[:, np.newaxis] *\
            dre_drho0_linear

        return derivative

    def del_log10re_del_chargeability(self, pars):
        r"""
        Calculate the derivate :math:`\frac{\partial
        log_{10}(\underline{-Im})}{\partial m_i}`

        Return an K x N vector.

        """
        pars = self.convert_parameters(pars)

        re = self.forward_log10re(pars)
        dre_dg_linear = self.del_re_del_chargeability(pars)

        derivative = 1 / np.log(10) * (1 / re)[:, np.newaxis] * dre_dg_linear

        return derivative
